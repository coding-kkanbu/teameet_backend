import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

pytestmark = pytest.mark.django_db


class TestVerifyNeisEmail(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="testuser@teameet.com",
            username="test",
            random_name="random name",
            password="testpass1234",
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_verify_neis_email(self):
        url = reverse("verify_neis_email")
        res = self.client.post(
            url,
            data={
                "neis_email": "testuser@sen.go.kr",
                "redirect_url": "http://frontend.com",
            },
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.data == {"message": "Email was successfully sent"}
        assert (
            get_user_model().objects.get(pk=self.user.id).neis_email
            == "testuser@sen.go.kr"
        )

    def test_invalid_neis_domain(self):
        url = reverse("verify_neis_email")
        res = self.client.post(
            url,
            data={
                "neis_email": "testuser@gmail.com",
                "redirect_url": "http://frontend.com",
            },
        )

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        self.assertRaises(ValidationError)

    def test_duplicate_neis_address(self):
        get_user_model().objects.create(
            email="testuser2@teameet.com",
            username="test2",
            random_name="another random name",
            password="testpass1234",
            is_verify=True,
            neis_email="testuser@sen.go.kr",
        )

        url = reverse("verify_neis_email")
        res = self.client.post(
            url,
            data={
                "neis_email": "testuser@sen.go.kr",
                "redirect_url": "http://frontend.com",
            },
        )

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        self.assertRaises(ValidationError)

    def test_not_verified_duplicate_neis_address(self):
        get_user_model().objects.create(
            email="testuser2@teameet.com",
            username="test2",
            random_name="another random name",
            password="testpass1234",
            is_verify=False,
            neis_email="testuser@sen.go.kr",
        )

        url = reverse("verify_neis_email")
        res = self.client.post(
            url,
            data={
                "neis_email": "testuser@sen.go.kr",
                "redirect_url": "http://frontend.com",
            },
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.data == {"message": "Email was successfully sent"}


class TestVerifyNeisEmailConfirm(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="testuser@teameet.com",
            username="test",
            random_name="random name",
            password="testpass1234",
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    @override_settings(FRONTEND_URL="http://frontend.com")
    def test_verify_neis_email_confirm(self):
        token = AccessToken.for_user(self.user)
        url = reverse_querystring(
            "verify_neis_email_confirm", query_kwargs={"token": token}
        )
        res = self.client.get(url)

        self.assertTrue(get_user_model().objects.get(pk=self.user.id).is_verify)
        self.assertRedirects(
            res,
            settings.FRONTEND_URL + "?token_valid=true",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False,
        )


def reverse_querystring(
    view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None
):
    """Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    """
    base_url = reverse(
        view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app
    )
    if query_kwargs:
        return "{}?{}".format(base_url, urlencode(query_kwargs))
    return base_url
