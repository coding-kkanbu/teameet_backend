from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from kkanbu.board.models import Category, Comment, Post


class NotificationViewSetTestData(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create(
            email="user1@teameet.com",
            username="user1",
            password="user1pass00",
        )
        cls.user2 = get_user_model().objects.create(
            email="user2@teameet.com",
            username="user2",
            password="user2pass00",
        )
        cat_topic = Category.objects.create(
            app="Topic", name="토픽 테스트", slug="topic_test"
        )
        cat_pitapat = Category.objects.create(
            app="PitAPat", name="핏어펫 테스트", slug="pitapat_test"
        )
        cls.post_topic = Post.objects.create(
            category=cat_topic,
            writer=cls.user1,
            title="Post1",
            content="Post1_content",
        )
        cls.post_pitapat = Post.objects.create(
            category=cat_pitapat,
            writer=cls.user2,
            title="Post2",
            content="Post2_content",
        )
        cls.comment1 = Comment.objects.create(
            comment="Comment1",
            post=cls.post_topic,
            writer=cls.user2,
        )
        cls.comment2 = Comment.objects.create(
            comment="Comment2",
            post=cls.post_pitapat,
            writer=cls.user1,
        )

        cls.user1_client = APIClient()
        cls.user2_client = APIClient()

        cls.user1_client.force_authenticate(user=cls.user1)
        cls.user2_client.force_authenticate(user=cls.user2)
