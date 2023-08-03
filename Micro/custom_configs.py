import nanoid
import secrets, os
from django.db.models import CharField
from django.conf import settings
from django.core.files.storage import FileSystemStorage

protected_storage = FileSystemStorage(location=str(settings.PROTECTED_MEDIA_ROOT))


def get_nano_id():
    return nanoid.generate(size=12)


def handle_product_attachment_upload(instance, filename):
    ext = filename.split(".")[-1]
    new_file_name = f"{secrets.token_hex(10)}.{ext}"
    return f"{instance.product.handle}/{new_file_name}"


