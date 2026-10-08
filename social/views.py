from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import CommentForm, PostForm
from .models import Comment, FriendshipRequest, Notification, Post, PostLike
from .utils.enums import FriendshipStatus, PostVisibility
from .utils.permissions import can_view_post

User = get_user_model()


def _safe_next(request, fallback):
    target = request.POST.get("next", "")
    if target and url_has_allowed_host_and_scheme(
        target, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return target
    return fallback


def _accepted_friends(user):
    sent = FriendshipRequest.objects.filter(sender=user, status=FriendshipStatus.ACCEPTED).values_list("recipient_id", flat=True)
    received = FriendshipRequest.objects.filter(recipient=user, status=FriendshipStatus.ACCEPTED).values_list("sender_id", flat=True)
    return User.objects.filter(Q(pk__in=sent) | Q(pk__in=received)).distinct()


def _post_context(posts, user):
    visible = [post for post in posts if can_view_post(user, post)]
    liked_ids = set()
    if getattr(user, "is_authenticated", False) and visible:
        liked_ids = set(PostLike.objects.filter(user=user, post_id__in=[p.pk for p in visible]).values_list("post_id", flat=True))
    return [{"post": post, "liked": post.pk in liked_ids, "comment_form": CommentForm()} for post in visible]


@login_required
def feed(request):
    friends = _accepted_friends(request.user).values_list("pk", flat=True)
    posts = Post.objects.filter(Q(author=request.user) | Q(author_id__in=friends)).select_related("author")
    page = Paginator(posts, 20).get_page(request.GET.get("page"))
    context = {
        "post_form": PostForm(),
        "feed_posts": _post_context(page.object_list, request.user),
        "page_obj": page,
        "friend_count": _accepted_friends(request.user).count(),
        "pending_request_count": FriendshipRequest.objects.filter(recipient=request.user, status=FriendshipStatus.PENDING).count(),
    }
    return render(request, "social/feed.html", context)


@login_required
def members(request):
    query = request.GET.get("q", "").strip()
    people = User.objects.exclude(pk=request.user.pk).order_by("first_name", "last_name", "email")
    if query:
        people = people.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query))
    friend_ids = set(_accepted_friends(request.user).values_list("pk", flat=True))
    sent = {r.recipient_id: r for r in FriendshipRequest.objects.filter(sender=request.user, status=FriendshipStatus.PENDING)}
    incoming = {r.sender_id: r for r in FriendshipRequest.objects.filter(recipient=request.user, status=FriendshipStatus.PENDING)}
    people = people.prefetch_related(Prefetch(
        "posts",
        queryset=Post.objects.filter(visibility=PostVisibility.PUBLIC).only(
            "id", "author_id", "content", "created_at", "visibility"
        ),
        to_attr="public_posts",
    ))
    page = Paginator(people, 20).get_page(request.GET.get("page"))
    return render(request, "social/members.html", {
        "people": page, "query": query, "friend_ids": friend_ids,
        "outgoing_ids": set(sent), "incoming_ids": set(incoming),
        "pending_request_count": len(incoming),
    })


@login_required
def friends(request):
    query = request.GET.get("q", "").strip()
    people = _accepted_friends(request.user).order_by("first_name", "last_name", "email")
    if query:
        people = people.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
        )
    page = Paginator(people, 20).get_page(request.GET.get("page"))
    return render(request, "social/friends.html", {
        "friends": page,
        "query": query,
        "page_obj": page,
        "friend_count": page.paginator.count,
        "pending_request_count": FriendshipRequest.objects.filter(recipient=request.user, status=FriendshipStatus.PENDING).count(),
    })


@login_required
def requests(request):
    incoming = FriendshipRequest.objects.filter(recipient=request.user, status=FriendshipStatus.PENDING).select_related("sender")
    outgoing = FriendshipRequest.objects.filter(sender=request.user, status=FriendshipStatus.PENDING).select_related("recipient")
    return render(request, "social/requests.html", {
        "incoming": incoming, "outgoing": outgoing,
        "pending_request_count": incoming.count(),
    })


@login_required
def notifications(request):
    notifications_list = Notification.objects.filter(recipient=request.user).select_related(
        "actor", "friendship_request"
    )[:100]
    return render(request, "social/notifications.html", {
        "notifications_list": notifications_list,
        "pending_request_count": FriendshipRequest.objects.filter(
            recipient=request.user, status=FriendshipStatus.PENDING
        ).count(),
    })


@login_required
@require_POST
def mark_notifications_read(request):
    Notification.objects.filter(recipient=request.user, read_at__isnull=True).update(
        read_at=timezone.now()
    )
    messages.success(request, "Vos notifications ont été marquées comme lues.")
    return redirect("social:notifications")


@login_required
def public_profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    if profile_user == request.user:
        return redirect("accounts:profile")
    relationship = FriendshipRequest.objects.filter(
        Q(sender=request.user, recipient=profile_user) | Q(sender=profile_user, recipient=request.user)
    ).order_by("-created_at").first()
    is_friend = _accepted_friends(request.user).filter(pk=profile_user.pk).exists()
    profile_posts = profile_user.posts.select_related("author")
    if not is_friend:
        profile_posts = profile_posts.filter(visibility=PostVisibility.PUBLIC)
    page = Paginator(profile_posts, 20).get_page(request.GET.get("page"))
    return render(request, "social/profile.html", {
        "profile_user": profile_user, "is_friend": is_friend,
        "relationship": relationship,
        "profile_posts": _post_context(page.object_list, request.user),
        "page_obj": page,
        "pending_request_count": FriendshipRequest.objects.filter(recipient=request.user, status=FriendshipStatus.PENDING).count(),
    })


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
    if not can_view_post(request.user, post):
        raise Http404
    return render(request, "social/post_detail.html", {
        "feed_posts": _post_context([post], request.user),
        "pending_request_count": FriendshipRequest.objects.filter(
            recipient=request.user, status=FriendshipStatus.PENDING
        ).count(),
    })


@login_required
@require_POST
def create_post(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Votre publication a été partagée.")
    else:
        messages.error(request, "La publication n’a pas pu être enregistrée. Vérifiez son contenu.")
    return redirect("social:feed")


@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author_id != request.user.pk and not request.user.has_perm("social.moderate_post"):
        raise Http404
    post.delete()
    messages.success(request, "La publication a été supprimée.")
    return redirect(_safe_next(request, "social:feed"))


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author_id != request.user.pk and not request.user.has_perm("social.moderate_post"):
        raise Http404
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Votre publication a été modifiée.")
        return redirect(_safe_next(request, "social:feed"))
    return render(request, "social/edit_post.html", {
        "form": form,
        "post": post,
        "pending_request_count": FriendshipRequest.objects.filter(recipient=request.user, status=FriendshipStatus.PENDING).count(),
    })


@login_required
@require_POST
def send_request(request, user_id):
    recipient = get_object_or_404(User, pk=user_id)
    if recipient.pk == request.user.pk:
        messages.error(request, "Vous ne pouvez pas vous inviter vous-même.")
        return redirect("social:members")
    existing = FriendshipRequest.objects.filter(
        Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user)
    ).order_by("-created_at").first()
    if existing and existing.status == FriendshipStatus.ACCEPTED:
        messages.info(request, "Vous êtes déjà amis.")
    elif existing and existing.status == FriendshipStatus.PENDING:
        if existing.recipient_id == request.user.pk:
            existing.status = FriendshipStatus.ACCEPTED
            existing.save(update_fields=("status", "updated_at"))
            messages.success(request, f"Vous êtes maintenant ami avec {recipient.get_full_name() or recipient.email}.")
        else:
            messages.info(request, "Une invitation est déjà en attente.")
    else:
        if existing:
            FriendshipRequest.objects.filter(
                Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user),
                status=FriendshipStatus.DECLINED,
            ).delete()
        FriendshipRequest.objects.create(sender=request.user, recipient=recipient)
        messages.success(request, "Votre invitation a été envoyée.")
    return redirect(_safe_next(request, "social:members"))


@login_required
@require_POST
def respond_request(request, request_id):
    friend_request = get_object_or_404(FriendshipRequest, pk=request_id, recipient=request.user, status=FriendshipStatus.PENDING)
    decision = request.POST.get("decision")
    if decision not in ("accept", "decline"):
        raise Http404
    friend_request.status = FriendshipStatus.ACCEPTED if decision == "accept" else FriendshipStatus.DECLINED
    friend_request.save(update_fields=("status", "updated_at"))
    messages.success(request, "Invitation acceptée." if decision == "accept" else "Invitation refusée.")
    return redirect("social:requests")


@login_required
@require_POST
def cancel_request(request, request_id):
    get_object_or_404(FriendshipRequest, pk=request_id, sender=request.user, status=FriendshipStatus.PENDING).delete()
    messages.success(request, "L’invitation a été annulée.")
    return redirect("social:requests")


@login_required
@require_POST
def remove_friend(request, user_id):
    friend = get_object_or_404(User, pk=user_id)
    FriendshipRequest.objects.filter(
        Q(sender=request.user, recipient=friend) | Q(sender=friend, recipient=request.user),
        status=FriendshipStatus.ACCEPTED,
    ).delete()
    messages.success(request, "Cet ami a été retiré de votre liste.")
    return redirect("social:friends")


@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
    if not can_view_post(request.user, post):
        raise Http404
    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect(_safe_next(request, "social:feed"))


@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
    if not can_view_post(request.user, post):
        raise Http404
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    else:
        messages.error(request, "Le commentaire ne peut pas être vide.")
    return redirect(_safe_next(request, "social:feed"))


@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment.objects.select_related("post"), pk=comment_id)
    if comment.author_id != request.user.pk and not request.user.has_perm("social.moderate_post"):
        raise Http404
    comment.delete()
    messages.success(request, "Le commentaire a été supprimé.")
    return redirect(_safe_next(request, "social:feed"))


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author_id != request.user.pk:
        raise Http404
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Le commentaire a été modifié.")
        return redirect(_safe_next(request, "social:feed"))
    return render(request, "social/edit_comment.html", {
        "form": form,
        "comment": comment,
        "pending_request_count": FriendshipRequest.objects.filter(
            recipient=request.user, status=FriendshipStatus.PENDING
        ).count(),
    })
