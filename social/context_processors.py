from .models import FriendshipRequest, Notification
from .utils.enums import FriendshipStatus


def social_navigation(request):
    if not request.user.is_authenticated:
        return {}
    return {
        "pending_request_count": FriendshipRequest.objects.filter(
            recipient=request.user, status=FriendshipStatus.PENDING
        ).count(),
        "unread_social_notification_count": Notification.objects.filter(
            recipient=request.user, read_at__isnull=True
        ).count(),
    }
