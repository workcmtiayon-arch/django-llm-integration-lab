import accounts.validators
import social.models
import social.storage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import migrations, models
from django.db import transaction


def move_post_images_to_private_storage(apps, schema_editor):
    Post = apps.get_model("social", "Post")
    private_storage = social.storage.private_post_storage
    for post in Post.objects.exclude(image="").iterator():
        old_name = post.image.name
        old_storage = post.image.storage
        if not old_storage.exists(old_name):
            continue
        with old_storage.open(old_name, "rb") as source:
            new_name = private_storage.save(old_name, ContentFile(source.read()))
        post.image.name = new_name
        post.save(update_fields=("image",))
        transaction.on_commit(lambda storage=old_storage, name=old_name: storage.delete(name))


def restore_post_images_to_public_storage(apps, schema_editor):
    Post = apps.get_model("social", "Post")
    private_storage = social.storage.private_post_storage
    for post in Post.objects.exclude(image="").iterator():
        old_name = post.image.name
        if not private_storage.exists(old_name):
            continue
        with private_storage.open(old_name, "rb") as source:
            new_name = default_storage.save(old_name, ContentFile(source.read()))
        post.image.name = new_name
        post.save(update_fields=("image",))
        transaction.on_commit(lambda storage=private_storage, name=old_name: storage.delete(name))


class Migration(migrations.Migration):
    dependencies = [("social", "0006_social_query_indexes")]

    operations = [
        migrations.RunPython(move_post_images_to_private_storage, restore_post_images_to_public_storage),
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True,
                storage=social.storage.private_post_storage,
                upload_to=social.models.post_image_upload_path,
                validators=[accounts.validators.validate_profile_image],
            ),
        ),
    ]
