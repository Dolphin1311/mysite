import tempfile
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def get_temporary_image(temp_file=tempfile.NamedTemporaryFile()):
    size = (200, 200)
    color = (153, 153, 255)
    image = Image.new("RGB", size, color)
    image.save(temp_file, 'png')

    return temp_file

def get_temp_dir():
    return tempfile.gettempdir()
