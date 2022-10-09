from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timesince
from rest_framework.test import APIClient

from kkanbu.board.models import Category, Comment, Post, SogaetingOption
from kkanbu.notification.models import Notification
from kkanbu.notification.tests.test_helper import NotificationViewSetTestData
from kkanbu.users.tests.factories import UserFactory


class PostModelTests(NotificationViewSetTestData):
    """Signal Tests"""

    def test_delete_noti_by_post_related_to_postlike_success(self):
        # create postlike noti
        url_postlike = reverse("api:Topic-toggle-postlike", args=[self.post_topic.pk])
        users = UserFactory.create_batch(8)
        for user in users:
            client = APIClient()
            client.force_authenticate(user)
            client.post(url_postlike)
        self.assertEqual(Notification.objects.count(), 8)
        # check is_show affact notification
        instance = Post.objects.get(id=self.post_topic.pk)
        instance.is_show = False
        instance.save()
        self.assertEqual(Notification.objects.count(), 0)

    def test_delete_noti_by_post_related_to_postblame_success(self):
        # create postlike noti
        url_postlike = reverse("api:Topic-toggle-postlike", args=[self.post_topic.pk])
        users = UserFactory.create_batch(5)
        for user in users:
            client = APIClient()
            client.force_authenticate(user)
            client.post(url_postlike)
        self.assertEqual(Notification.objects.count(), 5)
        # create postblame noti
        url_postblame = reverse("api:Topic-report-postblame", args=[self.post_topic.pk])
        payload = {"reason": "abuse", "description": "blaah blaah"}
        users = UserFactory.create_batch(5)
        for user in users:
            client = APIClient()
            client.force_authenticate(user)
            client.post(url_postblame, payload)
        # check is_show affact notification by postblame blind
        self.assertEqual(Notification.objects.count(), 1)

    """Constraints Tests"""

    def test_title_length_less_than_four_fail(self):
        self.post_topic.title = "abc"
        with self.assertRaises(IntegrityError):
            self.post_topic.save()

    def test_content_length_less_than_four_fail(self):
        self.post_topic.content = "3글자"
        with self.assertRaises(IntegrityError):
            self.post_topic.save()

    """Internal Function Tests"""

    def test_post_timesince_property(self):
        self.assertTrue(self.post_topic.timesince)
        ts = timesince.timesince(self.post_topic.created, depth=1)
        self.assertEqual(self.post_topic.timesince, ts)


class CommentModelTests(NotificationViewSetTestData):
    """Signal Tests"""

    def test_delete_noti_by_comment_related_to_commentlike_success(self):
        # create commentlike noti
        url_commentlike = reverse(
            "api:Comment-toggle-commentlike", args=[self.comment1.pk]
        )
        users = UserFactory.create_batch(8)
        for user in users:
            client = APIClient()
            client.force_authenticate(user)
            client.post(url_commentlike)
        self.assertEqual(Notification.objects.count(), 8)
        # check is_show affact notification
        instance = Comment.objects.get(id=self.comment1.pk)
        instance.is_show = False
        instance.save()
        self.assertEqual(Notification.objects.count(), 0)

    def test_delete_noti_by_comment_related_to_commentblame_success(self):
        # create commentlike noti
        url_commentlike = reverse(
            "api:Comment-toggle-commentlike", args=[self.comment1.pk]
        )
        users = UserFactory.create_batch(5)
        for user in users:
            client = APIClient()
            client.force_authenticate(user)
            client.post(url_commentlike)
        self.assertEqual(Notification.objects.count(), 5)
        # create commentblame noti
        url_commentblame = reverse(
            "api:Comment-report-commentblame", args=[self.comment1.pk]
        )
        payload = {"reason": "abuse", "description": "blaah blaah"}
        users = UserFactory.create_batch(3)
        for user in users:
            client = APIClient()
            client.force_authenticate(user)
            client.post(url_commentblame, payload)
        # check is_show affact notification by commentblame blind
        self.assertEqual(Notification.objects.count(), 1)

    """Constraints Tests"""

    def test_comment_length_less_than_four_fail(self):
        self.comment1.comment = "3글자"
        with self.assertRaises(IntegrityError):
            self.comment1.save()

    """Internal Function Tests"""

    def test_comment_timesince_property(self):
        self.assertTrue(self.comment1.timesince)
        ts = timesince.timesince(self.comment1.created, depth=1)
        self.assertEqual(self.comment1.timesince, ts)


class CategoryModelTests(TestCase):
    """Constraints Tests"""

    def test_app_type_choice_invalid_fail(self):
        cat = Category(
            app="app_type_invalid",
            name="올바르지 않은 앱타입",
            slug="app_type",
        )
        with self.assertRaises(IntegrityError):
            cat.save()

    def test_app_type_choice_valid_success(self):
        cat = Category(
            app="Topic",
            name="올바른 앱타입",
            slug="app_type",
        )
        cat.save()
        self.assertTrue(cat in Category.objects.all())


class SogaetingOptionModelTests(NotificationViewSetTestData):
    """Constraints Tests"""

    def test_region_choice_invalid_fail(self):
        sogae = SogaetingOption(
            post=self.post_pitapat,
            region="Seoul",
            gender=1,
            age=25,
        )
        with self.assertRaises(IntegrityError):
            sogae.save()

    def test_region_choice_valid_success(self):
        sogae = SogaetingOption.objects.create(
            post=self.post_pitapat,
            region="서울",
            gender=1,
            age=25,
        )
        self.assertTrue(sogae in SogaetingOption.objects.all())

    def test_gender_choice_invalid_fail(self):
        sogae = SogaetingOption(
            post=self.post_pitapat,
            region="서울",
            gender=4,
            age=25,
        )
        with self.assertRaises(IntegrityError):
            sogae.save()

    def test_age_less_than_twenty_fail(self):
        sogae = SogaetingOption(
            post=self.post_pitapat,
            region="서울",
            gender=1,
            age=15,
        )
        with self.assertRaises(IntegrityError):
            sogae.save()
