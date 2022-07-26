# from unittest.mock import MagicMock

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from kkanbu.accounts.views import get_redirect_url


class GoogleSocialLoginTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="testuser@teameet.com",
            username="test",
            random_name="random name",
            password="testpass1234",
        )
        self.client = APIClient()
        self.social_client_id = "1234_client_id_4321"
        self.social_secret = "1234_client_secret_4321"

        self.socialapp_googl = SocialApp.objects.create(
            provider="google",
            name="google_test",
            client_id=self.social_client_id,
            secret=self.social_secret,
        )

    def test_google_login_redirect(self):
        url = reverse("google_login")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        try:
            scope = settings.SOCIALACCOUNT_PROVIDERS["google"]["SCOPE"]
        except KeyError:
            scope = None
        url = get_redirect_url(
            GoogleOAuth2Adapter, "google", settings.GOOGLE_CALLBACK_URI, scope
        )
        self.assertEqual(res.data["url"], url)

    # def test_google_callback(self):
    #     if social_url is correct:
    #         return code
    #     MagicMock().return_value()
    #     url = reverse("google_callback")
    #     res = self.client.get(url)


class KakaoSocialLoginTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="testuser@teameet.com",
            username="test",
            random_name="random name",
            password="testpass1234",
        )
        self.client = APIClient()
        self.social_client_id = "1234_client_id_4321"
        self.social_secret = "1234_client_secret_4321"

        self.socialapp_kakao = SocialApp.objects.create(
            provider="kakao",
            name="kakao_test",
            client_id=self.social_client_id,
            secret=self.social_secret,
        )

    def test_kakao_login_redirect(self):
        url = reverse("kakao_login")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        try:
            scope = settings.SOCIALACCOUNT_PROVIDERS["kakao"]["SCOPE"]
        except KeyError:
            scope = None
        url = get_redirect_url(
            KakaoOAuth2Adapter, "kakao", settings.KAKAO_CALLBACK_URI, scope
        )
        self.assertEqual(res.data["url"], url)
