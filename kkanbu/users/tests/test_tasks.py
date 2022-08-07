import pytest
from celery.result import EagerResult
from django.contrib.auth import get_user_model

from kkanbu.users.tasks import get_users_count
from kkanbu.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_count(settings):
    """A basic test to execute the get_users_count Celery task."""
    get_user_model().objects.all().delete()
    UserFactory.create_batch(3)
    settings.CELERY_TASK_ALWAYS_EAGER = True
    task_result = get_users_count.delay()
    assert isinstance(task_result, EagerResult)
    assert task_result.result == 3
