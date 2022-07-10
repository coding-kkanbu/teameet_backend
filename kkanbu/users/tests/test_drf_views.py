import pytest
from django.test import RequestFactory

from kkanbu.users.api.views import UserViewSet
from kkanbu.users.models import User

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    def test_get_queryset(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)
        res_data = response.data
        res_data.pop("date_joined")
        assert res_data == {
            "id": user.pk,
            "username": user.username,
            "email": user.email,
            "random_name": user.random_name,
            "profile_image": user.profile_image,
            "neis_email": user.neis_email,
            "is_verify": user.is_verify,
            "post_n": 0,
            "url": f"http://testserver/api/v1/users/{user.username}/",
        }
