from http.cookies import SimpleCookie

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class CustomJWTCookieAuthenticationTests(TestCase):
    def setUp(self):
        self.api_client = APIClient()

    def test_valid_token_http_header_authentication_success(self):
        # acquire  token
        url = reverse("account_signup")
        payload = {
            "email": "test@test.com",
            "username": "testuser",
            "password1": "asdf4321",
            "password2": "asdf4321",
        }
        res = self.api_client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # token authenticate by HTTP header
        access = res.data["access_token"]
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + access)

        url_auth = reverse("api:Topic-list")
        res = self.api_client.get(url_auth)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_invalid_token_http_header_authentication_fail(self):
        access = "invalid_token"
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + access)

        url_auth = reverse("api:Topic-list")
        res = self.api_client.get(url_auth)
        self.assertEqual(
            res.status_code, status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED
        )

    def test_valid_token_cookie_authentication_success(self):
        # acquire  token
        url = reverse("account_signup")
        payload = {
            "email": "test@test.com",
            "username": "testuser",
            "password1": "asdf4321",
            "password2": "asdf4321",
        }
        res = self.api_client.post(url, payload)

        # token authenticate by Cookie
        cookie_name = getattr(settings, "JWT_AUTH_COOKIE", None)
        access = res.data["access_token"]
        self.api_client.cookies = SimpleCookie({cookie_name: access})

        url_auth = reverse("api:Topic-list")
        res = self.api_client.get(url_auth)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_invalid_token_cookie_authentication_fail(self):
        cookie_name = getattr(settings, "JWT_AUTH_COOKIE", None)
        invalid_access = "thisisnotatoken"
        self.api_client.cookies = SimpleCookie({cookie_name: invalid_access})

        url_auth = reverse("api:Topic-list")
        res = self.api_client.get(url_auth)
        self.assertEqual(
            res.status_code, status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED
        )
