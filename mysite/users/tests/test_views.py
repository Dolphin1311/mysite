from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.models import User


class TestViews(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            email="test_email@mail.com",
            password="testPassw0rd1",
        )
        self.request_factory = RequestFactory()
        self.client = Client()
        self.login_url = reverse("login")
        self.signup_url = reverse("signup")
        self.logout_url = reverse("logout")
        self.orders_url = reverse("user_orders")

    def test_login(self):
        response = self.client.post(
            self.login_url,
            data={
                "email": "test_email@mail.com",
                "password": "testPassw0rd1",
            }
        )

        self.assertTrue(response.status_code, 302)

    def test_signup(self):
        # get
        response = self.client.get(self.signup_url)

        self.assertTemplateUsed(response, "users/user_registration.html")
        self.assertEqual(response.status_code, 200)

        # post
        post_data = {
            "email": "test_register_email@mail.com",
            "password1": "testPassw0rd1",
            "password2": "testPassw0rd1"
        }
        response = self.client.post(self.signup_url, data=post_data)
        user = User.objects.get(email="test_register_email@mail.com")

        self.assertTrue(response.status_code, 302)
        self.assertTrue(isinstance(user, User))

    def test_logout(self):
        response = self.client.get(self.logout_url)
        self.assertTrue(response.status_code, 200)

    def test_user_cabinet_orders(self):
        response = self.client.post(
            self.orders_url,
            data={
                "end_user": "owner",
                "status": True
            }
        )

        self.assertEqual(response.status_code, 302)
