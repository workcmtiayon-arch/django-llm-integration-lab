from django.db import transaction
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from social.models import FriendshipRequest, Notification, Post
from .enums import FriendshipStatus


@receiver(post_save, sender=FriendshipRequest)
def notify_friendship_change(sender, instance, created, **kwargs):
    if instance.status == FriendshipStatus.PENDING:
        Notification.objects.filter(friendship_request=instance).delete()
        Notification.objects.create(
            recipient=instance.recipient,
            actor=instance.sender,
            kind=Notification.Kind.FRIEND_REQUEST,
            friendship_request=instance,
        )
    elif instance.status == FriendshipStatus.ACCEPTED:
        Notification.objects.get_or_create(
            recipient=instance.sender,
            actor=instance.recipient,
            kind=Notification.Kind.FRIEND_ACCEPTED,
            friendship_request=instance,
        )


@receiver(pre_save, sender=Post)
def remember_previous_post_image(sender, instance, **kwargs):
    if not instance.pk:
        instance._previous_image = ""
        return
    instance._previous_image = sender.objects.filter(pk=instance.pk).values_list(
        "image", flat=True
    ).first() or ""


@receiver(post_save, sender=Post)
def remove_replaced_post_image(sender, instance, **kwargs):
    previous = getattr(instance, "_previous_image", "")
    if previous and previous != instance.image.name:
        storage = instance.image.storage
        transaction.on_commit(lambda: storage.delete(previous))


@receiver(pre_delete, sender=Post)
def remember_deleted_post_image(sender, instance, **kwargs):
    if instance.image:
        storage = instance.image.storage
        name = instance.image.name
        transaction.on_commit(lambda: storage.delete(name))
