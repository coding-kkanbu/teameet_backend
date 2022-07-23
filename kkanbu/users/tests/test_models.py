import pytest

from kkanbu.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_user_random_name(user: User):
    assert user.random_name == "잘난 카멜레온"
