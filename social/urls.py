from django.urls import path

from . import views

app_name = "social"

urlpatterns = [
    path("", views.feed, name="feed"),
    path("membres/", views.members, name="members"),
    path("amis/", views.friends, name="friends"),
    path("invitations/", views.requests, name="requests"),
    path("notifications/", views.notifications, name="notifications"),
    path("notifications/lues/", views.mark_notifications_read, name="mark_notifications_read"),
    path("profil/<int:user_id>/", views.public_profile, name="profile"),
    path("publications/<int:post_id>/", views.post_detail, name="post_detail"),
    path("publications/creer/", views.create_post, name="create_post"),
    path("publications/<int:post_id>/supprimer/", views.delete_post, name="delete_post"),
    path("publications/<int:post_id>/modifier/", views.edit_post, name="edit_post"),
    path("publications/<int:post_id>/aimer/", views.toggle_like, name="toggle_like"),
    path("publications/<int:post_id>/commenter/", views.add_comment, name="add_comment"),
    path("invitations/envoyer/<int:user_id>/", views.send_request, name="send_request"),
    path("invitations/<int:request_id>/repondre/", views.respond_request, name="respond_request"),
    path("invitations/<int:request_id>/annuler/", views.cancel_request, name="cancel_request"),
    path("amis/<int:user_id>/retirer/", views.remove_friend, name="remove_friend"),
]
