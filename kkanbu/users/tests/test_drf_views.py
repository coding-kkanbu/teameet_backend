import os
import tempfile

import pytest
from django.test import RequestFactory
from django.urls import reverse
from faker import Faker
from PIL import Image
from rest_framework import status
from rest_framework.serializers import DateTimeField

from kkanbu.users.api.views import UserViewSet
from kkanbu.users.models import User

from .factories import PostFactory, UserFactory

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    def test_get_queryset(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request
        assert user in view.get_queryset()

    def test_get_user_detail(self, user: User, api_client):
        api_client.force_authenticate(user)
        url = reverse("api:user-detail", kwargs={"username": user.username})
        res = api_client.get(url)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == {
            "id": user.pk,
            "username": user.username,
            "email": user.email,
            "date_joined": DateTimeField().to_representation(user.date_joined),
            "random_name": user.random_name,
            "introduce": "좋은 만남을 기대하고있습니다",
            "profile_image": user.profile_image,
            "neis_email": user.neis_email,
            "is_verify": user.is_verify,
            "post_n": 0,
            "url": f"http://testserver/api/v1/users/{user.username}/",
        }

    # TODO ImageFields static_file 설정 및 연결 후 테스트 코드 추가 필요
    def test_put_user_detail(self, user: User, api_client):
        api_client.force_authenticate(user)
        url = reverse("api:user-detail", kwargs={"username": user.username})
        payload = {"username": "testuser", "introduce": "서울에서 근무하는 초등교사입니다. 만나서 반갑습니다."}
        res = api_client.put(url, payload)
        assert res.status_code == status.HTTP_200_OK
        assert User.objects.filter(pk=user.id).get().introduce == payload["introduce"]

    def test_patch_user_detail(self, user: User, api_client):
        api_client.force_authenticate(user)
        url = reverse("api:user-detail", kwargs={"username": user.username})
        fake = Faker()
        new_username = fake.simple_profile()["username"]
        payload = {"username": new_username}
        res = api_client.patch(url, payload)
        assert res.status_code == status.HTTP_200_OK
        assert User.objects.filter(username=new_username).exists() is True

        url = reverse("api:user-detail", kwargs={"username": new_username})
        res = api_client.get(url)
        assert res.status_code == status.HTTP_200_OK

    # TODO force_authenticate 대신 JWT access tokeon을 Hearder에 넣어서 인증하는 방식으로
    #      로그인 된 user에 대해 테스트 진행 / delete 이후 detail view 안되는 것 테스트 추가
    def test_delete_user(self, api_client):
        payload = {
            "email": "test@teameet.com",
            "username": "testuser",
            "password": "testpass1234",
        }
        user = UserFactory.create(
            email=payload["email"],
            username=payload["username"],
            password=payload["password"],
        )
        assert (
            api_client.login(email=payload["email"], password=payload["password"])
            is True
        )
        assert user.is_active is True

        url = reverse("api:user-detail", kwargs={"username": user.username})
        api_client.force_authenticate(user)
        res = api_client.delete(url)
        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert (
            api_client.login(email=payload["email"], password=payload["password"])
            is False
        )
        user.refresh_from_db()
        assert user.is_active is False

    def test_my_posts_retrieve(self, user: User, api_client):
        api_client.force_authenticate(user)
        url = reverse("api:user-my-posts", kwargs={"username": user.username})
        PostFactory.create_batch(8, writer=user)

        res = api_client.get(url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data["results"]) == 8

    def test_my_posts_filter_is_show(self, user: User, api_client):
        api_client.force_authenticate(user)
        url = reverse("api:user-my-posts", kwargs={"username": user.username})
        PostFactory.create_batch(5, writer=user, is_show=False)

        res = api_client.get(url)
        assert len(res.data["results"]) == 0

    def test_my_posts_pagination(self, user: User, api_client):
        api_client.force_authenticate(user)
        url = reverse("api:user-my-posts", kwargs={"username": user.username})
        PostFactory.create_batch(25, writer=user)

        res = api_client.get(url)
        assert res.data["count"] == 25

        res = api_client.get(url, **{"QUERY_STRING": "page=3"})
        res.status_code == 200
        assert len(res.data["results"]) == 5

    def test_set_random_name(self, user: User, api_client):
        api_client.force_authenticate(user)
        old_random_name = user.random_name

        url = reverse("api:user-set-random-name", kwargs={"username": user.username})
        res = api_client.post(url)
        new_random_name = res.data["random_name"]

        assert User.objects.get(pk=user.id).random_name == new_random_name
        assert res.status_code == 200
        assert old_random_name != new_random_name

    def test_upload_image(self, user: User, api_client):
        api_client.force_authenticate(user)
        url = reverse("api:user-upload-image", kwargs={"username": user.username})
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"profile_image": image_file}
            res = api_client.post(url, payload, format="multipart")

        user.refresh_from_db()
        assert res.status_code == 200
        assert "profile_image" in res.data
        assert os.path.exists(user.profile_image.path) is True

    def test_upload_image_bad_request(self, user: User, api_client):
        api_client.force_authenticate(user)
        url = reverse("api:user-upload-image", kwargs={"username": user.username})
        payload = {"profile_image": "NotAnImage"}
        res = api_client.post(url, payload, format="multipart")

        assert res.status_code == 400
