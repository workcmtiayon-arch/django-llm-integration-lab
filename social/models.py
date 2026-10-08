from uuid import uuid4

from PIL import Image
from django.conf import settings
from django.db import models
from django.db.models import Q

from .core.models import TimeStampedModel
from .utils.enums import FriendshipStatus, PostVisibility
from accounts.validators import validate_profile_image


def post_image_upload_path(instance, filename):
    with Image.open(instance.image.file) as image:
        extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}[image.format]
    return f"posts/{instance.author_id}/{uuid4().hex}.{extension}"


class FriendshipRequest(TimeStampedModel):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="friendship_requests_sent",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="friendship_requests_received",
    )
    status = models.CharField(
        max_length=12, choices=FriendshipStatus.choices,
        default=FriendshipStatus.PENDING, db_index=True,
    )

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(fields=("sender", "recipient"), name="unique_friendship_direction"),
            models.CheckConstraint(condition=~Q(sender=models.F("recipient")), name="friendship_not_self"),
        ]

    def __str__(self):
        return f"{self.sender} → {self.recipient} ({self.get_status_display()})"


class Post(TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=5000)
    image = models.ImageField(upload_to=post_image_upload_path, blank=True, validators=[validate_profile_image])
    visibility = models.CharField(
        max_length=10, choices=PostVisibility.choices, default=PostVisibility.PUBLIC,
    )

    class Meta:
        ordering = ("-created_at",)
        permissions = [("moderate_post", "Can moderate posts")]

    def __str__(self):
        return f"Publication de {self.author} ({self.created_at:%Y-%m-%d})"

class PostLike(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_likes")

    class Meta:
        constraints = [models.UniqueConstraint(fields=("post", "user"), name="unique_post_like")]


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=1000)

    class Meta:
        ordering = ("created_at",)


class Notification(TimeStampedModel):
    class Kind(models.TextChoices):
        FRIEND_REQUEST = "friend_request", "Invitation reçue"
        FRIEND_ACCEPTED = "friend_accepted", "Invitation acceptée"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="social_notifications")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="social_actions")
    kind = models.CharField(max_length=20, choices=Kind.choices)
    friendship_request = models.ForeignKey(
        FriendshipRequest, on_delete=models.CASCADE, related_name="notifications",
    )
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)
        constraints = [models.UniqueConstraint(fields=("recipient", "actor", "kind", "friendship_request"), name="unique_social_notification")]
