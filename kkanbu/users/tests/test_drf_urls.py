import pytest
from django.urls import resolve, reverse

from kkanbu.users.models import User

pytestmark = pytest.mark.django_db


def test_user_list():
    assert reverse("api:user-list") == "/api/v1/users/"
    assert resolve("/api/v1/users/").view_name == "api:user-list"


def test_user_detail(user: User):
    assert (
        reverse("api:user-detail", kwargs={"username": user.username})
        == f"/api/v1/users/{user.username}/"
    )
    assert resolve(f"/api/v1/users/{user.username}/").view_name == "api:user-detail"


def test_user_my_posts(user: User):
    assert (
        reverse("api:user-my-posts", kwargs={"username": user.username})
        == f"/api/v1/users/{user.username}/my_posts/"
    )
    assert (
        resolve(f"/api/v1/users/{user.username}/my_posts/").view_name
        == "api:user-my-posts"
    )


def test_user_set_random_name(user: User):
    assert (
        reverse("api:user-set-random-name", kwargs={"username": user.username})
        == f"/api/v1/users/{user.username}/set_random_name/"
    )
    assert (
        resolve(f"/api/v1/users/{user.username}/set_random_name/").view_name
        == "api:user-set-random-name"
    )
