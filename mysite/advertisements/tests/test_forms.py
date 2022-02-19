from django.test import TestCase
from django.contrib.auth import get_user_model
from advertisements.models import (
    AdvertisingSpaceCategory,
    AdvertisingSpace,
    AdvertisingSpaceImage,
)
from advertisements.forms import AdvertisingSpaceForm, AdvertisingSpaceImagesFormSet
from advertisements.tests import helper_utils
from users.models import UserType


class TestForms(TestCase):
    def setUp(self):
        # set user object
        user_model = get_user_model()
        user_type = UserType.objects.create(name="test user")
        self.user = user_model.objects.create(
            email="test_email@email.com", password="test_Pass1234", user_type=user_type
        )

        # set advertising space category object
        self.adv_space_category = AdvertisingSpaceCategory.objects.create(
            name="test category"
        )
        self.adv_space = AdvertisingSpace.objects.create(
            title="Test title",
            description="Test description",
            data={
                "car_model": "test data 1",
                "prod_year": "test data 2",
                "car_type": "test data 3",
                "adv_place": "test data 3",
            },
            is_published=True,
            user=self.user,
            price="12",
            advertising_space_category=self.adv_space_category,
        )

    def test_advertising_space_form_is_valid(self):
        form_data = {
            "title": "test title",
            "description": "test desc",
            "car_model": "test model",
            "prod_year": 2000,
            "car_type": "test type",
            "adv_place": "top",
            "price": 20.1,
            "advertising_space_category": self.adv_space_category,
            "user": self.user,
        }
        form = AdvertisingSpaceForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_advertising_space_image_formset_is_valid(self):
        formset_data = {
            "images-TOTAL_FORMS": 1,
            "images-INITIAL_FORMS": 0,
            "images-MIN_NUM_FORMS": 0,
            "images-MAX_NUM_FORMS": 1,
            "images-0-image": helper_utils.get_temporary_image(),
        }
        formset = AdvertisingSpaceImagesFormSet(formset_data)

        self.assertTrue(formset.is_valid())
