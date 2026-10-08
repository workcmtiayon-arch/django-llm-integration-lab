from uuid import uuid4

from PIL import Image
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_profile_image


def profile_photo_upload_path(instance, filename):
    with Image.open(instance.profile_photo.file) as image:
        extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}[image.format]
    return f"profiles/{instance.pk}/{uuid4().hex}.{extension}"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        email = (email or "").strip()
        if not email:
            raise ValueError("An email address is required.")

        email = self.normalize_email(email).casefold()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("A superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("A superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    profile_photo = models.ImageField(
        upload_to=profile_photo_upload_path,
        blank=True,
        validators=[validate_profile_image],
    )
    bio = models.CharField("biography", max_length=280, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
