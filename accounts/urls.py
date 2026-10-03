"""URL namespace for account and authentication views."""

from django.contrib.auth import views as auth_views
from django.urls import path

from .views import ProfileUpdateView, ProfileView, RegistrationView

app_name = "accounts"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", RegistrationView.as_view(), name="register"),
]
