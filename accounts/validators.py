"""Validation helpers for user supplied profile images."""

from PIL import Image, UnidentifiedImageError
from django.core.exceptions import ValidationError

MAX_PROFILE_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_PROFILE_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}


def validate_profile_image(upload):
    if upload.size > MAX_PROFILE_IMAGE_SIZE:
        raise ValidationError("The profile image must be 5 MB or smaller.")

    try:
        upload.seek(0)
        with Image.open(upload) as image:
            if image.format not in ALLOWED_PROFILE_IMAGE_FORMATS:
                raise ValidationError("Use a JPEG, PNG, or WebP image.")
            image.verify()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValidationError("Upload a valid JPEG, PNG, or WebP image.") from exc
    finally:
        upload.seek(0)
