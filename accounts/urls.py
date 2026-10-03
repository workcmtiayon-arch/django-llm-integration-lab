"""URL namespace for account and authentication views."""

from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .views import (
    ProfilePhotoUpdateView,
    ProfileUpdateView,
    ProfileView,
    RegistrationView,
)

app_name = "accounts"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/photo/", ProfilePhotoUpdateView.as_view(), name="profile_photo"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password/change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
            success_url=reverse_lazy("accounts:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password/change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("register/", RegistrationView.as_view(), name="register"),
]
