from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from advertisements.models import AdvertisingSpace, AdvertisingSpaceCategory
from advertisements.tests import helper_utils
from advertisements.views import AdvSpaceCreateView
from users.models import UserType


class TestViews(TestCase):
    def setUp(self):
        # set user object
        user_model = get_user_model()
        user_type = UserType.objects.create(name="test user")
        self.user = user_model.objects.create(
            email="test_email@email.com",
            password="test_Pass1234",
            user_type=user_type
        )

        # set advertising space object
        self.adv_space_category = AdvertisingSpaceCategory.objects.create(name="Test category")
        self.adv_space = AdvertisingSpace.objects.create(
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
            advertising_space_category=self.adv_space_category
        )

        # set necessary vars for testing
        self.client = Client()
        self.request_factory = RequestFactory()
        self.list_url = reverse("adv_spaces")
        self.detail_url = reverse("adv_space", kwargs={"adv_space_slug": self.adv_space.slug})
        self.create_url = reverse("add_adv_space")
        self.update_url = reverse("edit_adv_space", kwargs={"adv_space_slug": self.adv_space.slug})

    def test_adv_spaces_list_GET(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "advertisements/advertising_spaces.html")

    def test_adv_space_detail_GET(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "advertisements/advertising_space.html")

    def test_adv_space_create_GET(self):
        response = self.client.get(self.create_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "advertisements/create_advertising_space.html")

    def test_adv_space_create_POST(self):
        post_data = {
            "title": "test title",
            "description": "test desc",
            "car_model": "test model",
            "prod_year": 2000,
            "car_type": "test type",
            "adv_place": "top",
            "price": 20.1,
            "user": self.user,
            "advertising_space_category": self.adv_space_category.id,
            "images-TOTAL_FORMS": 1,
            "images-INITIAL_FORMS": 0,
            "images-MIN_NUM_FORMS": 0,
            "images-MAX_NUM_FORMS": 1,
            "images-0-image": helper_utils.get_temporary_image().name
        }

        self.client.force_login(user=self.user)  # login user
        request = self.request_factory.post(self.create_url, data=post_data, format="multipart")
        request.user = self.user
        response = AdvSpaceCreateView.as_view()(request)
        response.client = self.client

        self.assertRedirects(response, reverse("user_cabinet"))

    def test_adv_space_update_GET(self):
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "advertisements/update_advertising_space.html")

