import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("social", "0002_post_image"), ("accounts", "0005_user_bio")]

    operations = [
        migrations.RemoveConstraint(
            model_name="notification",
            name="unique_social_notification",
        ),
        migrations.AlterField(
            model_name="notification",
            name="kind",
            field=models.CharField(choices=[("friend_request", "Invitation reçue"), ("friend_accepted", "Invitation acceptée"), ("post_like", "Publication aimée"), ("post_comment", "Nouveau commentaire")], max_length=20),
        ),
        migrations.AlterField(
            model_name="notification",
            name="friendship_request",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to="social.friendshiprequest"),
        ),
        migrations.AddField(
            model_name="notification",
            name="post",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to="social.post"),
        ),
        migrations.AddConstraint(
            model_name="notification",
            constraint=models.UniqueConstraint(fields=("recipient", "actor", "kind", "friendship_request", "post"), name="unique_social_notification"),
        ),
    ]
