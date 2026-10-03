"""URL namespace for account and authentication views."""

from django.urls import path

from .views import RegistrationView

app_name = "accounts"

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
]
