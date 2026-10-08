from django.apps import AppConfig


class SocialConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "social"
    verbose_name = "Réseau social"

    def ready(self):
        from .utils import signals  # noqa: F401

