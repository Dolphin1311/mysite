from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings


class AdvertisingSpaceType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length='255', unique=True, db_index=True, verbose_name='URL')


class AdvertisingSpace(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    slug = models.SlugField(max_length='255', unique=True, db_index=True, verbose_name='URL')
    data = JSONField(verbose_name='Data')
    is_published = models.BooleanField(default=True, verbose_name='Is published')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date updated')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='User id')
    advertising_space_type = models.ForeignKey(
        AdvertisingSpaceType,
        on_delete=models.PROTECT,
        verbose_name='Advertising space type'
    )


class AdvertisingSpaceImage(models.Model):
    image =

