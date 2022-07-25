from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class TestAllAuthViews(APITestCase):
    USERNAME = "person"
    PASS = "personfakepassword"
    EMAIL = "person1@world.com"
    NEW_PASS = "new-test-pass"

    def setUp(self):
        self.register_url = reverse("account_signup")
        self.login_url = reverse("account_login")
        self.logout_url = reverse("account_logout")
        self.client = APIClient()

    def test_registration(self):
        REGISTRATION_DATA = {
            "email": self.EMAIL,
            "username": self.USERNAME,
            "password1": self.PASS,
            "password2": self.PASS,
        }
        user_count = get_user_model().objects.all().count()

        result = self.client.post(
            self.register_url, data=REGISTRATION_DATA, status_code=201
        )

        self.assertIn("access_token", result.data)
        self.assertEqual(get_user_model().objects.all().count(), user_count + 1)

    def test_login(self):
        LOGIN_DATA = {
            "email": self.EMAIL,
            "password": self.PASS,
        }
        get_user_model().objects.create_user(
            email=self.EMAIL,
            username=self.USERNAME,
            password=self.PASS,
        )

        result = self.client.post(self.login_url, data=LOGIN_DATA, status_code=200)

        self.assertIn("access_token", result.data)
