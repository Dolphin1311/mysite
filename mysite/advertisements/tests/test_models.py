import init_test_env
import os

init_test_env.init_test_env()

from django.test import TestCase
from django.utils.text import slugify
from advertisements.models import AdvertisingSpace, AdvertisingSpaceCategory, AdvertisingSpaceImage
from users.models import User, UserType
from django.utils import timezone
from django.db.models import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile


class AdvertisingSpaceTest(TestCase):
    def create_user(self):
        UserType.objects.create(name="Test user type")
        return User.objects.create(
            email="test_email@email.com",
            password="test_Pass1234",
            user_type=UserType.objects.get(name="Test user type")
        )

    def create_advertising_space(self):
        AdvertisingSpaceCategory.objects.create(name="Test category")
        return AdvertisingSpace.objects.create(
            title="Test title",
            description="Test description",
            data=dict(data1="test data 1", data2="test data 2", data3="test data 3"),
            is_published=True,
            date_created=timezone.now(),
            date_updated=timezone.now(),
            user=self.create_user(),
            price="12",
            advertising_space_category=AdvertisingSpaceCategory.objects.get(name="Test category")
        )

    def create_advertising_space_image(self, adv_space=None, image_path=None):
        # if no adv_space in args, then create new
        if adv_space:
            _adv_space = adv_space
        else:
            _adv_space = self.create_advertising_space()

        if image_path:
            _image_path = image_path
        else:
            _image_path = "images/test_image.jpg"

        return AdvertisingSpaceImage.objects.create(
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=open(_image_path, "rb").read(),
                content_type="image/jpeg"
            ),
            advertising_space=_adv_space
        )

    def test_advertising_space_creation(self):
        adv_space = self.create_advertising_space()

        self.assertTrue(isinstance(adv_space, AdvertisingSpace))
        self.assertEqual(adv_space.slug, slugify(adv_space.title))
        adv_space.delete()

    def test_advertising_space_deletion(self):
        adv_space = self.create_advertising_space()
        adv_space.delete()
        self.assertRaises(ObjectDoesNotExist, AdvertisingSpace.objects.get, pk=adv_space.pk)

    def test_advertising_space_get_image(self):
        adv_space = self.create_advertising_space()
        adv_space_image = self.create_advertising_space_image(adv_space)

        self.assertEqual(adv_space.get_image().image, adv_space_image.image)

    def test_advertising_space_image_creation(self):
        adv_space_image = self.create_advertising_space_image()

        self.assertTrue(isinstance(adv_space_image, AdvertisingSpaceImage))
        adv_space_image.delete()

    def test_advertising_space_image_deletion(self):
        adv_space_image = self.create_advertising_space_image()
        adv_space_image.delete()

        self.assertRaises(ObjectDoesNotExist, AdvertisingSpace.objects.get, pk=adv_space_image.pk)

    def test_deletion_advertising_space_image_when_advertising_space_deleting(self):
        adv_space = self.create_advertising_space()
        adv_space_image = self.create_advertising_space_image(adv_space)
        adv_space_image.delete()

        self.assertRaises(ObjectDoesNotExist, AdvertisingSpace.objects.get, pk=adv_space_image.pk)

    def test_delete_image_from_os_lib(self):
        image_path = "images/test_image_delete.jpg"
        adv_space_image = self.create_advertising_space_image(image_path=image_path)
        image_path_md5 = adv_space_image.image.path
        adv_space_image.delete()

        self.assertFalse(os.path.exists(image_path_md5))
