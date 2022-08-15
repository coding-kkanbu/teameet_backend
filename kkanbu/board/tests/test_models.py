from django.urls import reverse
from rest_framework.test import APIClient

from kkanbu.board.models import Comment, Post
from kkanbu.notification.models import Notification
from kkanbu.notification.tests.test_helper import NotificationViewSetTestData
from kkanbu.users.tests.factories import UserFactory


class PostModelSignalTests(NotificationViewSetTestData):
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


class CommentModelSignalTests(NotificationViewSetTestData):
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
