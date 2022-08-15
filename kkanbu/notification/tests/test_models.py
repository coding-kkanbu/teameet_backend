from kkanbu.notification.models import Notification
from kkanbu.notification.tests.test_helper import NotificationViewSetTestData
from kkanbu.operation.models import CommentBlame, CommentLike, PostBlame, PostLike


class NotificationModelTests(NotificationViewSetTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.commentlike = CommentLike.objects.create(
            comment=cls.comment1, user=cls.user1
        )
        cls.commentblame = CommentBlame.objects.create(
            comment=cls.comment1, user=cls.user1
        )
        cls.postlike_topic = PostLike.objects.create(
            post=cls.post_topic, user=cls.user1
        )
        cls.postlike_pitapat = PostLike.objects.create(
            post=cls.post_pitapat, user=cls.user1
        )
        cls.postblame_topic = PostBlame.objects.create(
            post=cls.post_topic, user=cls.user2
        )
        cls.postblame_pitapat = PostBlame.objects.create(
            post=cls.post_pitapat, user=cls.user2
        )

    def setUp(self):
        self.comment_noti = Notification.objects.create(
            notification_type="comment",
            content_object=self.comment1,
            recipient=self.user1,
            message="noti message",
        )

        self.commentlike_noti = Notification.objects.create(
            notification_type="commentlike",
            content_object=self.commentlike,
            recipient=self.user1,
            message="noti message",
        )

        self.commentblame_noti = Notification.objects.create(
            notification_type="commentblame",
            content_object=self.commentblame,
            recipient=self.user1,
            message="noti message",
        )

        self.postlike_topic_noti = Notification.objects.create(
            notification_type="postlike",
            content_object=self.postlike_topic,
            recipient=self.user2,
            message="noti message",
        )

        self.postlike_pitapat_noti = Notification.objects.create(
            notification_type="postlike",
            content_object=self.postlike_pitapat,
            recipient=self.user2,
            message="noti message",
        )

        self.postblame_topic_noti = Notification.objects.create(
            notification_type="postblame",
            content_object=self.postblame_topic,
            recipient=self.user1,
            message="noti message",
        )

        self.postblame_pitapat_noti = Notification.objects.create(
            notification_type="postblame",
            content_object=self.postblame_pitapat,
            recipient=self.user1,
            message="noti message",
        )

    def test_get_absolute_url_success(self):
        self.assertEqual(
            self.comment_noti.get_absolute_url(),
            f"/api/v1/comment/{self.comment1.pk}/",
        )
        self.assertEqual(
            self.commentlike_noti.get_absolute_url(),
            f"/api/v1/comment/{self.comment1.pk}/",
        )
        self.assertEqual(
            self.commentblame_noti.get_absolute_url(),
            f"/api/v1/comment/{self.comment1.pk}/",
        )
        self.assertEqual(
            self.postlike_topic_noti.get_absolute_url(),
            f"/api/v1/topic/{self.post_topic.pk}/",
        )
        self.assertEqual(
            self.postlike_pitapat_noti.get_absolute_url(),
            f"/api/v1/pitapat/{self.post_pitapat.pk}/",
        )
        self.assertEqual(
            self.postblame_topic_noti.get_absolute_url(),
            f"/api/v1/topic/{self.post_topic.pk}/",
        )
        self.assertEqual(
            self.postblame_pitapat_noti.get_absolute_url(),
            f"/api/v1/pitapat/{self.post_pitapat.pk}/",
        )

    def test_get_absolute_url_exception(self):
        Notification.objects.create(
            notification_type="invalid_type",
            content_object=self.postblame_topic,
            recipient=self.user1,
            message="noti message",
        )
        self.assertRaises(Exception)
