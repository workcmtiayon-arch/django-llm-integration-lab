from .enums import FriendshipStatus, PostVisibility


def can_view_post(user, post):
    """Public posts are readable by anyone; friends posts require accepted friendship."""
    if post.visibility == PostVisibility.PUBLIC:
        return True
    if not getattr(user, "is_authenticated", False):
        return False
    if user.pk == post.author_id:
        return True
    return post.author.friendship_requests_sent.filter(
        recipient=user, status=FriendshipStatus.ACCEPTED
    ).exists() or post.author.friendship_requests_received.filter(
        sender=user, status=FriendshipStatus.ACCEPTED
    ).exists()
