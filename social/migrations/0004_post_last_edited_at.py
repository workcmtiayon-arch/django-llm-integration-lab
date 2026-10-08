from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("social", "0003_engagement_notifications")]

    operations = [
        migrations.AddField(
            model_name="post",
            name="last_edited_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
