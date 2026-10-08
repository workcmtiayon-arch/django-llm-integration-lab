from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("social", "0005_post_reports")]

    operations = [
        migrations.AddIndex(
            model_name="friendshiprequest",
            index=models.Index(fields=["recipient", "status", "-created_at"], name="friend_inbox_idx"),
        ),
        migrations.AddIndex(
            model_name="friendshiprequest",
            index=models.Index(fields=["sender", "status", "-created_at"], name="friend_outbox_idx"),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(fields=["author", "-created_at"], name="post_author_time_idx"),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(fields=["visibility", "-created_at"], name="post_visibility_time_idx"),
        ),
        migrations.AddIndex(
            model_name="notification",
            index=models.Index(fields=["recipient", "read_at", "-created_at"], name="social_notification_idx"),
        ),
    ]
