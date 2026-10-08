from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class PrivatePostStorage(FileSystemStorage):
    """Store post media outside MEDIA_ROOT so static media serving cannot expose it."""

    def __init__(self):
        super().__init__(location=settings.PRIVATE_MEDIA_ROOT)


private_post_storage = PrivatePostStorage()
