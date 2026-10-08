# Initial social network schema.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0004_alter_user_profile_photo"),
    ]

    operations = [
        migrations.CreateModel(
            name="FriendshipRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("status", models.CharField(choices=[("pending", "En attente"), ("accepted", "Acceptée"), ("declined", "Refusée")], db_index=True, default="pending", max_length=12)),
                ("recipient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="friendship_requests_received", to=settings.AUTH_USER_MODEL)),
                ("sender", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="friendship_requests_sent", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("content", models.TextField(max_length=5000)),
                ("visibility", models.CharField(choices=[("public", "Tout le monde"), ("friends", "Amis uniquement")], default="public", max_length=10)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="posts", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",), "permissions": [("moderate_post", "Can moderate posts")]},
        ),
        migrations.CreateModel(
            name="PostLike",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to="social.post")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="post_likes", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("content", models.CharField(max_length=1000)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to=settings.AUTH_USER_MODEL)),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="social.post")),
            ],
            options={"ordering": ("created_at",)},
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("kind", models.CharField(choices=[("friend_request", "Invitation reçue"), ("friend_accepted", "Invitation acceptée")], max_length=20)),
                ("read_at", models.DateTimeField(blank=True, null=True)),
                ("actor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="social_actions", to=settings.AUTH_USER_MODEL)),
                ("friendship_request", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to="social.friendshiprequest")),
                ("recipient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="social_notifications", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.AddConstraint(
            model_name="friendshiprequest",
            constraint=models.UniqueConstraint(fields=("sender", "recipient"), name="unique_friendship_direction"),
        ),
        migrations.AddConstraint(
            model_name="friendshiprequest",
            constraint=models.CheckConstraint(condition=~models.Q(sender=models.F("recipient")), name="friendship_not_self"),
        ),
        migrations.AddConstraint(
            model_name="postlike",
            constraint=models.UniqueConstraint(fields=("post", "user"), name="unique_post_like"),
        ),
        migrations.AddConstraint(
            model_name="notification",
            constraint=models.UniqueConstraint(fields=("recipient", "actor", "kind", "friendship_request"), name="unique_social_notification"),
        ),
    ]
