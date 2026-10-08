import accounts.validators
import social.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("social", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(blank=True, upload_to=social.models.post_image_upload_path, validators=[accounts.validators.validate_profile_image]),
        ),
    ]
