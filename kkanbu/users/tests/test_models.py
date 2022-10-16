import pytest

from kkanbu.users import models
from kkanbu.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_profile_file_path():
    """Test generating image path."""
    file_path = models.profile_image_file_path(None, "example.jpg")
    assert file_path == "uploads/profile/example.jpg"
