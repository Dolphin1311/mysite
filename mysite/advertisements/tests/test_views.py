from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from advertisements.models import AdvertisingSpace, AdvertisingSpaceCategory
from users.models import UserType


class TestViews(TestCase):
    def setUp(self):
        # set user object
        user_model = get_user_model()
        user_type = UserType.objects.create(name="test user")
        user = user_model.objects.create(
            email="test_email@email.com",
            password="test_Pass1234",
            user_type=user_type
        )

        # set advertising space object
        AdvertisingSpaceCategory.objects.create(name="Test category")
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
            user=user,
            price="12",
            advertising_space_category=AdvertisingSpaceCategory.objects.get(name="Test category")
        )

        # set necessary vars for testing
        self.client = Client()
        self.list_url = reverse("adv_spaces")
        self.detail_url = reverse("adv_space", kwargs={"adv_space_slug": self.adv_space.slug})
        self.update_url = reverse("edit_adv_space", kwargs={"adv_space_slug": self.adv_space.slug})

    def test_adv_spaces_list_GET(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "advertisements/advertising_spaces.html")

    def test_adv_space_detail_GET(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "advertisements/advertising_space.html")

    def test_adv_space_update_GET(self):
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "advertisements/update_advertising_space.html")
