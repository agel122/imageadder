import hashlib

from PIL import Image
import io

from django.core.files.base import ContentFile


def resize_rename(file, width, height=None):
    file_to_save = io.BytesIO()
    image = Image.open(file)
    if height is None:
        wpercent = (width/float(image.size[0]))
        height = int((float(image.size[1])*float(wpercent)))
    image_resized = image.resize((width, height))
    image_resized.save(file_to_save, 'png')
    file_to_save.seek(0)

    name_to_hash = file.name.split('.')[0]
    hash_name = hashlib.md5(name_to_hash.encode()).hexdigest()
    name_to_save = f'{hash_name}_{width}x{height}.png'
    django_friendly_file = ContentFile(file.read(), name_to_save)

    return django_friendly_file


