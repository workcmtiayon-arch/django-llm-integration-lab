from django.db import models


class FriendshipStatus(models.TextChoices):
    PENDING = "pending", "En attente"
    ACCEPTED = "accepted", "Acceptée"
    DECLINED = "declined", "Refusée"


class PostVisibility(models.TextChoices):
    PUBLIC = "public", "Tout le monde"
    FRIENDS = "friends", "Amis uniquement"

