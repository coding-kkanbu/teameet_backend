from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from kkanbu.board.helpers.utils import get_client_ip
from kkanbu.board.models import Comment, Post
from kkanbu.board.serializers import CommentSerializer
from kkanbu.users.tests.factories import (
    CategoryFactory,
    CommentFactory,
    PostFactory,
    UserFactory,
)


class TestComment(APITestCase):
    """Test Comment endpoint API"""

    def setUp(self):
        self.user1, self.user2 = UserFactory.create_batch(2)

        self.category = CategoryFactory.create(app="Topic")

        self.post1 = PostFactory.create(category=self.category, writer=self.user1)
        self.post1 = PostFactory.create(category=self.category, writer=self.user2)

        self.client = APIClient()
        self.request_factory = APIRequestFactory()
        self.client.force_authenticate(self.user1)

    def test_create_comment(self):
        """Test comment create"""
        payload = {
            "post": self.post1.id,
            "parent_comment": "",
            "comment": "test comment",
            "secret": False,
            "is_show": True,
        }
        url = reverse("api:Comment-list")
        request = self.request_factory.post(url, payload)
        res = self.client.post(url, data=payload)
        comment = Comment.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment.comment, payload["comment"])
        self.assertEqual(comment.writer, self.user1)
        self.assertEqual(comment.ip, get_client_ip(request))

    def test_retrieve_comment(self):
        """Test comment retrieve"""
        comment = CommentFactory.create()
        url = reverse("api:Comment-detail", args=[comment.id])
        request = self.request_factory.get("./fake_path")
        request.user = self.user1
        res = self.client.get(url)
        serializer = CommentSerializer(comment, context={"request": request})
        self.assertEqual(res.data, serializer.data)

    def test_post_get_comments(self):
        """Test getting comment list from post"""
        CommentFactory.create_batch(20, post=self.post1)
        request = self.request_factory.get("./fake_path")
        request.user = self.user1
        url = reverse("api:Topic-get-comments", args=[self.post1.id])
        res = self.client.get(url)

        comments_queryset = Post.objects.get(
            pk=self.post1.id
        ).comment_set.get_queryset()
        serializer = CommentSerializer(
            comments_queryset, context={"request": request}, many=True
        )

        self.assertEqual(serializer.data, res.data)
