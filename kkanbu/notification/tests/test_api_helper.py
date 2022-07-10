from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from kkanbu.board.models import Category, Comment, Post


class NotificationViewSetTestData(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create(
            email="user1@teameet.com",
            username="user1",
            random_name="random name 1",
            password="user1pass00",
        )
        cls.user2 = get_user_model().objects.create(
            email="user2@teameet.com",
            username="user2",
            random_name="random name 2",
            password="user2pass00",
        )
        cat = Category.objects.create(name="테스트1")
        post1 = Post.objects.create(
            category=cat,
            writer=cls.user1,
            title="Post1",
            content="Post1_content",
        )
        post2 = Post.objects.create(
            category=cat,
            writer=cls.user2,
            title="Post2",
            content="Post2_content",
        )
        cls.comment1 = Comment.objects.create(
            comment="Comment1",
            post=post1,
            writer=cls.user2,
        )
        cls.comment2 = Comment.objects.create(
            comment="Comment2",
            post=post2,
            writer=cls.user1,
        )

        cls.user1_client = APIClient()
        cls.user2_client = APIClient()

        cls.user1_client.force_authenticate(user=cls.user1)
        cls.user2_client.force_authenticate(user=cls.user2)
