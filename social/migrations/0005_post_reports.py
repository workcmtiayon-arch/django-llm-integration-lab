import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("social", "0004_post_last_edited_at")]

    operations = [
        migrations.CreateModel(
            name="PostReport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("reason", models.CharField(choices=[("spam", "Spam ou publicité"), ("abuse", "Harcèlement ou contenu abusif"), ("misinformation", "Information trompeuse"), ("other", "Autre motif")], max_length=20)),
                ("details", models.CharField(blank=True, max_length=500)),
                ("status", models.CharField(choices=[("open", "À examiner"), ("reviewing", "En cours d’examen"), ("resolved", "Traité"), ("dismissed", "Classé sans suite")], db_index=True, default="open", max_length=12)),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reports", to="social.post")),
                ("reporter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="social_reports", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.AddConstraint(
            model_name="postreport",
            constraint=models.UniqueConstraint(fields=("reporter", "post"), name="unique_post_report"),
        ),
    ]
