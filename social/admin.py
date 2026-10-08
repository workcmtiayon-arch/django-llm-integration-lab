from django.contrib import admin
from django import forms

from .models import Comment, FriendshipRequest, Notification, Post, PostLike, PostReport


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


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        widgets = {"image": forms.FileInput}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ("author", "visibility", "created_at")
    list_filter = ("visibility", "created_at")
    search_fields = ("author__email", "content")
    readonly_fields = ("created_at", "updated_at", "image_name")
    inlines = (CommentInline,)

    @admin.display(description="Fichier image privé")
    def image_name(self, obj):
        return obj.image.name or "—"


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


@admin.register(PostReport)
class PostReportAdmin(admin.ModelAdmin):
    list_display = ("post", "reporter", "reason", "status", "created_at")
    list_filter = ("status", "reason", "created_at")
    search_fields = ("reporter__email", "post__author__email", "post__content", "details")
    readonly_fields = ("reporter", "post", "reason", "details", "created_at", "updated_at")
    actions = ("mark_reviewing", "mark_resolved", "dismiss_reports")

    @admin.action(description="Marquer les signalements en cours d’examen")
    def mark_reviewing(self, request, queryset):
        queryset.update(status="reviewing")

    @admin.action(description="Marquer les signalements comme traités")
    def mark_resolved(self, request, queryset):
        queryset.update(status="resolved")

    @admin.action(description="Classer les signalements sans suite")
    def dismiss_reports(self, request, queryset):
        queryset.update(status="dismissed")
