from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("accounts", "0004_alter_user_profile_photo")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="bio",
            field=models.CharField(blank=True, max_length=280, verbose_name="biography"),
        ),
    ]
