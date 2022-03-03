from django.test import TestCase
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    def test_create_user(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(email="test_email@mail.com", password="testPassw0rd1")
        self.assertEqual(user.email, "test_email@mail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            user_model.objects.create_user()

    def test_create_superuser(self):
        user_model = get_user_model()
        admin_user = user_model.objects.create_superuser(email='super@user.com', password='testAdminPaSs1')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)
