from django.db import models


class FriendshipStatus(models.TextChoices):
    PENDING = "pending", "En attente"
    ACCEPTED = "accepted", "Acceptée"
    DECLINED = "declined", "Refusée"


class PostVisibility(models.TextChoices):
    PUBLIC = "public", "Tout le monde"
    FRIENDS = "friends", "Amis uniquement"


class ReportReason(models.TextChoices):
    SPAM = "spam", "Spam ou publicité"
    ABUSE = "abuse", "Harcèlement ou contenu abusif"
    MISINFORMATION = "misinformation", "Information trompeuse"
    OTHER = "other", "Autre motif"


class ReportStatus(models.TextChoices):
    OPEN = "open", "À examiner"
    REVIEWING = "reviewing", "En cours d’examen"
    RESOLVED = "resolved", "Traité"
    DISMISSED = "dismissed", "Classé sans suite"
