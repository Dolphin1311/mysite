import tempfile
import os

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.db.models import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from PIL import Image
from advertisements.models import AdvertisingSpace, AdvertisingSpaceCategory, AdvertisingSpaceImage
from users.models import UserType


class TestModels(TestCase):
    def setUp(self):
        user_model = get_user_model()
        UserType.objects.create(name="test user")
        self.user = user_model.objects.create(
            email="test_email@email.com",
            password="test_Pass1234",
            user_type=UserType.objects.get(name="test user")
        )

    def get_temporary_image(self, temp_file):
        size = (200, 200)
        color = (255, 0, 0, 0)
        image = Image.new("RGBA", size, color)
        image.save(temp_file, 'png')
        return temp_file

    def create_advertising_space(self):
        AdvertisingSpaceCategory.objects.create(name="Test category")
        return AdvertisingSpace.objects.create(
            title="Test title",
            description="Test description",
            data={
                "car_model": "test data 1",
                "prod_year": "test data 2",
                "car_type": "test data 3",
                "adv_place": "test data 3"
            },
            is_published=True,
            date_created=timezone.now(),
            date_updated=timezone.now(),
            user=self.user,
            price="12",
            advertising_space_category=AdvertisingSpaceCategory.objects.get(name="Test category")
        )

    def create_advertising_space_image(self, adv_space=None):
        # if no adv_space in args, then create new
        if adv_space:
            _adv_space = adv_space
        else:
            _adv_space = self.create_advertising_space()

        # create test image
        temp_file = tempfile.NamedTemporaryFile()
        test_image = self.get_temporary_image(temp_file)

        return AdvertisingSpaceImage.objects.create(
            image=test_image.name,
            advertising_space=_adv_space
        )

    # AdvertisingSpace model
    def test_advertising_space_creation(self):
        adv_space = self.create_advertising_space()

        self.assertTrue(isinstance(adv_space, AdvertisingSpace))
        self.assertEqual(adv_space.slug, slugify(adv_space.title))
        self.assertEqual(reverse("adv_space", kwargs={"adv_space_slug": adv_space.slug}), adv_space.get_absolute_url())

    def test_advertising_space_deletion(self):
        adv_space = self.create_advertising_space()
        adv_space.delete()
        self.assertRaises(ObjectDoesNotExist, AdvertisingSpace.objects.get, pk=adv_space.pk)

    def test_advertising_space_get_image(self):
        adv_space = self.create_advertising_space()
        adv_space_image = self.create_advertising_space_image(adv_space)

        self.assertEqual(adv_space.get_image().image, adv_space_image.image)

    # AdvertisingSpaceImage model
    def test_advertising_space_image_creation(self):
        adv_space_image = self.create_advertising_space_image()

        self.assertTrue(isinstance(adv_space_image, AdvertisingSpaceImage))

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_advertising_space_image_deletion(self):
        adv_space_image = self.create_advertising_space_image()
        adv_space_image.delete()

        self.assertRaises(ObjectDoesNotExist, AdvertisingSpace.objects.get, pk=adv_space_image.pk)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_deletion_advertising_space_image_when_advertising_space_deleting(self):
        adv_space = self.create_advertising_space()
        adv_space_image = self.create_advertising_space_image(adv_space)
        adv_space_image.delete()

        self.assertRaises(ObjectDoesNotExist, AdvertisingSpace.objects.get, pk=adv_space_image.pk)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_delete_image_from_os_lib_when_advertising_space_image_deleting(self):
        adv_space_image = self.create_advertising_space_image()
        image_path_md5 = adv_space_image.image.path
        adv_space_image.delete()

        self.assertFalse(os.path.exists(image_path_md5))
