from django.db.models.signals import post_save
from django.dispatch import receiver

from social.models import FriendshipRequest, Notification
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
