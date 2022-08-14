import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient, APITestCase

from kkanbu.accounts.tokens import neis_verify_token

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
                "neis_email": "testuser@teameet.com",
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

    def test_verify_neis_email_confirm(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = neis_verify_token.make_token(self.user)
        url = reverse("verify_neis_email_confirm", args=[uid, token])
        res = self.client.get(url)

        self.assertTrue(get_user_model().objects.get(pk=self.user.id).is_verify)
        assert res.data == {"message": "Neis Email was successfully verified"}
        assert res.status_code == status.HTTP_200_OK

    def test_verify_neis_email_not_valid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = neis_verify_token.make_token(self.user)
        url = reverse("verify_neis_email_confirm", args=[uid, token[:-5]])
        res = self.client.get(url)

        self.assertFalse(get_user_model().objects.get(pk=self.user.id).is_verify)
        assert res.data == {"message": "Not valid token"}
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_verify_neis_email_not_valid_user(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = neis_verify_token.make_token(self.user)
        url = reverse("verify_neis_email_confirm", args=[uid + "E", token])
        res = self.client.get(url)

        self.assertFalse(get_user_model().objects.get(pk=self.user.id).is_verify)
        assert res.data == {"message": "Not valid user"}
        assert res.status_code == status.HTTP_400_BAD_REQUEST
