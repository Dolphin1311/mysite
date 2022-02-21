import os
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import JSONField
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from .utils import random_string_generator, path_and_rename


class AdvertisingSpaceCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(AdvertisingSpaceCategory, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name).capitalize()


class AdvertisingSpace(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )
    data = JSONField(verbose_name="Data")
    is_published = models.BooleanField(default=True, verbose_name="Is published")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Date updated")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User id"
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.01,
        validators=[MinValueValidator(0.01)],
    )
    advertising_space_category = models.ForeignKey(
        AdvertisingSpaceCategory,
        on_delete=models.CASCADE,
        verbose_name="Advertising space type",
    )

    def get_absolute_url(self):
        return reverse("adv_space", kwargs={"adv_space_slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = self.unique_slug_generator()
        super(AdvertisingSpace, self).save(*args, **kwargs)

    def unique_slug_generator(self, new_slug=None):
        """
        Create slug for model. If created slug is exists on some object of the model,
        then take this slug and add random string to the end of the slug.
        """
        if new_slug is not None:
            slug = new_slug
        else:
            slug = slugify(self.title)

        class_obj = self.__class__
        qs_exists = class_obj.objects.filter(slug=slug).exists()
        if qs_exists:
            new_slug = "{slug}-{randstr}".format(
                slug=slug, randstr=random_string_generator(size=4)
            )
            return self.unique_slug_generator(new_slug=new_slug)
        return slug

    def get_image(self):
        """ Return first image from AdvertisingSpaceImage model of selected object """
        return self.images.first()


class AdvertisingSpaceImage(models.Model):
    image = models.ImageField(
        upload_to=path_and_rename, verbose_name="Image", null=True, blank=True
    )
    advertising_space = models.ForeignKey(
        AdvertisingSpace,
        on_delete=models.CASCADE,
        verbose_name="Adverting space",
        related_name="images",
    )


@receiver(post_delete, sender=AdvertisingSpaceImage)
def post_delete_image(sender, instance, **kwargs):
    """ Delete image file on delete AdvertisingSpaceImage model object"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=AdvertisingSpaceImage)
def pre_delete_image_on_update(sender, instance, **kwargs):
    """ Delete old image file on update AdvertisingSpaceImage model object """
    if not instance.pk:
        return False

    old_image = AdvertisingSpaceImage.objects.get(pk=instance.pk).image
    new_image = instance.image
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
