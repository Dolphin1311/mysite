from django.db import models
from django.db.models import JSONField
from django.conf import settings
from django.urls import reverse

import hashlib
import os


class AdvertisingSpaceCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('space-type', kwargs={'category_slug': self.slug})


class AdvertisingSpace(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    data = JSONField(verbose_name='Data')
    is_published = models.BooleanField(default=True, verbose_name='Is published')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date updated')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='User id')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    advertising_space_category = models.ForeignKey(
        AdvertisingSpaceCategory,
        on_delete=models.PROTECT,
        verbose_name='Advertising space type'
    )


# functions for correctly storing images in AdvertisingSpaceImage model
def path_and_rename(instance, filename_base: str, deep_level=3):
    """
    Create whole filepath string to the storing image based on changed filename
    :param instance: instance of class
    :param filename_base: filename before editing
    :param deep_level: number of levels of nesting of folders
    :return: string of the whole path to the storing image
    """
    file_name, file_extension = os.path.splitext(filename_base)
    path = 'photos/'
    count_letters = 2
    filename = get_md5_file(file_name)

    for i in range(deep_level):
        path += filename[count_letters-2:count_letters] + '/'
        count_letters += 2

    filename += file_extension

    return os.path.join(path, filename)


def get_md5_file(filename):
    """
    Create md5 hash string based on filename
    :param filename: filename
    :return: string of md5 hash
    """
    result = hashlib.md5(filename.encode()).hexdigest()

    return result


class AdvertisingSpaceImage(models.Model):
    image = models.ImageField(upload_to=path_and_rename, verbose_name='Image', null=True, blank=True)
    advertising_space = models.ForeignKey(
        AdvertisingSpace,
        on_delete=models.PROTECT,
        verbose_name='Adverting space'
    )

    def get_absolute_url(self):
        return reverse('home')
