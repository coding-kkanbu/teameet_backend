from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework.test import APIClient

from kkanbu.notification.models import Notification
from kkanbu.notification.tests.test_helper import NotificationViewSetTestData
from kkanbu.operation.models import CommentBlame, CommentLike, PostBlame, PostLike
from kkanbu.users.tests.factories import UserFactory


class AbstractViewSetNotificationTests(NotificationViewSetTestData):
    def test_toggle_postlike_notification_send_and_delete_success(self):
        url = reverse("api:Topic-toggle-postlike", args=[self.post_topic.pk])
        # attempt 1st when create
        self.user1_client.post(url)
        # querying notification instance
        postlike = PostLike.objects.filter(post=self.post_topic, user=self.user1)[0]
        ctype = ContentType.objects.get_for_model(PostLike)
        noti_pre = Notification.objects.filter(
            notification_type="postlike",
            content_type=ctype,
            object_id=postlike.pk,
        )
        # noti send successfully
        self.assertTrue(noti_pre.exists())

        # attempt 2nd when delete
        self.user1_client.post(url)
        noti_post = Notification.objects.filter(
            notification_type="postlike",
            content_type=ctype,
            object_id=postlike.pk,
        )
        # noti delete successfully
        self.assertFalse(noti_post.exists())

    def test_report_postblame_notification_send_and_delete_success(self):
        url = reverse("api:Topic-report-postblame", args=[self.post_topic.pk])
        payload = {"reason": "abuse", "description": "blaah blaah"}
        # attempt fourth time
        users = UserFactory.create_batch(4)
        client = APIClient()
        for user in users:
            client.force_authenticate(user)
            client.post(url, payload)
        # querying notification instance
        postblame = PostBlame.objects.filter(post=self.post_topic, user=users[-1])[0]
        ctype = ContentType.objects.get_for_model(PostBlame)
        noti_post = Notification.objects.filter(
            notification_type="postblame",
            content_type=ctype,
            object_id=postblame.pk,
        )
        # noti not send yet
        self.assertFalse(noti_post.exists())

        # attempt fifth time when blind
        self.user2_client.post(url, payload)
        # querying notification instance
        postblame = PostBlame.objects.filter(post=self.post_topic, user=self.user2)[0]
        ctype = ContentType.objects.get_for_model(PostBlame)
        noti_post = Notification.objects.filter(
            notification_type="postblame",
            content_type=ctype,
            object_id=postblame.pk,
        )
        # noti send successfully
        self.assertTrue(noti_post.exists())
        self.assertEqual(
            noti_post[0].message,
            "회원님의 게시물이 신고 횟수 초과로 블라인드 처리되었습니다.",
        )


class CommentViewSetNotificationTests(NotificationViewSetTestData):
    def test_toggle_commentlike_notification_send_and_delete_success(self):
        url = reverse("api:Comment-toggle-commentlike", args=[self.comment1.pk])
        # attempt 1st when create
        self.user1_client.post(url)
        # querying notification instance
        commentlike = CommentLike.objects.filter(
            comment=self.comment1, user=self.user1
        )[0]
        ctype = ContentType.objects.get_for_model(CommentLike)
        noti_pre = Notification.objects.filter(
            notification_type="commentlike",
            content_type=ctype,
            object_id=commentlike.pk,
        )
        # noti send successfully
        self.assertTrue(noti_pre.exists())

        # attempt 2nd when delete
        self.user1_client.post(url)
        noti_post = Notification.objects.filter(
            notification_type="commentlike",
            content_type=ctype,
            object_id=commentlike.pk,
        )
        # noti delete successfully
        self.assertFalse(noti_post.exists())

    def test_report_commentblame_notification_send_and_delete_success(self):
        url = reverse("api:Comment-report-commentblame", args=[self.comment1.pk])
        payload = {"reason": "abuse", "description": "blaah blaah"}
        # attempt second time
        users = UserFactory.create_batch(2)
        client = APIClient()
        for user in users:
            client.force_authenticate(user)
            client.post(url, payload)
        # querying notification instance
        commentblame = CommentBlame.objects.filter(
            comment=self.comment1, user=users[-1]
        )[0]
        ctype = ContentType.objects.get_for_model(CommentBlame)
        noti_post = Notification.objects.filter(
            notification_type="commentblame",
            content_type=ctype,
            object_id=commentblame.pk,
        )
        # noti not send yet
        self.assertFalse(noti_post.exists())

        # attempt third time time when blind
        self.user1_client.post(url, payload)
        # querying notification instance
        commentblame = CommentBlame.objects.filter(
            comment=self.comment1, user=self.user1
        )[0]
        ctype = ContentType.objects.get_for_model(CommentBlame)
        noti_post = Notification.objects.filter(
            notification_type="commentblame",
            content_type=ctype,
            object_id=commentblame.pk,
        )
        # noti send successfully
        self.assertTrue(noti_post.exists())
        self.assertEqual(
            noti_post[0].message,
            "회원님의 댓글이 신고 횟수 초과로 블라인드 처리되었습니다.",
        )
