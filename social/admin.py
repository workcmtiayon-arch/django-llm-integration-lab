from django.contrib import admin

from .models import Comment, FriendshipRequest, Notification, Post, PostLike


@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("sender__email", "recipient__email")
    readonly_fields = ("created_at", "updated_at")


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("created_at", "updated_at")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "visibility", "created_at")
    list_filter = ("visibility", "created_at")
    search_fields = ("author__email", "content")
    readonly_fields = ("created_at", "updated_at")
    inlines = (CommentInline,)


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")
    search_fields = ("user__email", "post__content")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "actor", "kind", "read_at", "created_at")
    list_filter = ("kind", "read_at")
    search_fields = ("recipient__email", "actor__email")
    readonly_fields = ("created_at", "updated_at")
