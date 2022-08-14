from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
        self.post2 = PostFactory.create(category=self.category, writer=self.user2)

        self.request_factory = APIRequestFactory()
        self.client1 = APIClient()
        self.client1.force_authenticate(self.user1)
        self.client2 = APIClient()
        self.client2.force_authenticate(self.user2)

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
        res = self.client1.post(url, data=payload)
        comment = Comment.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment.comment, payload["comment"])
        self.assertEqual(comment.writer, self.user1)
        self.assertEqual(comment.ip, get_client_ip(request))

    def test_create_comment_different_post_comment_validation(self):
        """Test comment creation on different post comment"""
        parent_comment = CommentFactory.create(post=self.post1, writer=self.user2)
        payload = {
            "post": self.post2.id,
            "parent_comment": parent_comment.id,
            "comment": "test comment",
            "secret": False,
            "is_show": True,
        }
        url = reverse("api:Comment-list")
        res = self.client1.post(url, data=payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        self.assertRaises(ValidationError)

    def test_retrieve_comment(self):
        """Test comment retrieve"""
        comment = CommentFactory.create()
        url = reverse("api:Comment-detail", args=[comment.id])
        request = self.request_factory.get("./fake_path")
        request.user = self.user1
        res = self.client1.get(url)
        serializer = CommentSerializer(comment, context={"request": request})
        self.assertEqual(res.data, serializer.data)

    def test_post_get_comments(self):
        """Test getting comment list from post"""
        CommentFactory.create_batch(20, post=self.post1)
        request = self.request_factory.get("./fake_path")
        request.user = self.user1
        url = reverse("api:Topic-get-comments", args=[self.post1.id])
        res = self.client1.get(url)

        comments_queryset = Post.objects.get(
            pk=self.post1.id
        ).comment_set.get_queryset()
        serializer = CommentSerializer(
            comments_queryset, context={"request": request}, many=True
        )

        self.assertEqual(serializer.data, res.data)

    def test_secret_comment(self):
        """Test if secret comment is hidden to another person"""
        # post1 writer is user1
        comment = CommentFactory.create(
            post=self.post1,
            writer=self.user2,
            secret=True,
            is_show=True,
            parent_comment=None,
        )
        # complete stranger
        user3 = UserFactory.create()
        api_client3 = APIClient()
        api_client3.force_authenticate(user3)

        url = reverse("api:Topic-get-comments", args=[self.post1.id])
        res1 = self.client1.get(url)
        res2 = self.client2.get(url)
        res3 = api_client3.get(url)

        comment_res1 = [item for item in res1.data if item["id"] == comment.id][0]
        comment_res2 = [item for item in res2.data if item["id"] == comment.id][0]
        comment_res3 = [item for item in res3.data if item["id"] == comment.id][0]
        self.assertEqual(comment_res1["comment"], "이것은 댓글입니다.")
        self.assertEqual(comment_res2["comment"], "이것은 댓글입니다.")
        self.assertEqual(comment_res3["comment"], "[글 작성자와 댓글 작성자만 볼 수 있는 댓글입니다]")

    def test_secret_parent_comment(self):
        """Test getting secret comment is shown to the writer of parent comment"""
        # complete stranger
        user3 = UserFactory.create()
        api_client3 = APIClient()
        api_client3.force_authenticate(user3)

        # post1 writer is user1
        parent_comment = CommentFactory.create(
            post=self.post1, writer=self.user2, parent_comment=None, is_show=True
        )
        # secret child comment by another stranger
        comment = CommentFactory.create(
            post=self.post1, secret=True, is_show=True, parent_comment=parent_comment
        )

        url = reverse("api:Topic-get-comments", args=[self.post1.id])
        res2 = self.client2.get(url)
        res3 = api_client3.get(url)

        # 부모댓글 -> 자식댓글 조회
        parent_comment_res2 = [
            item for item in res2.data if item["id"] == parent_comment.id
        ][0]
        comment_from_res2 = [
            item
            for item in parent_comment_res2["child_comments"]
            if item["id"] == comment.id
        ][0]
        # 부모댓글 -> 자식댓글 조회
        parent_comment_res3 = [
            item for item in res3.data if item["id"] == parent_comment.id
        ][0]
        comment_from_res3 = [
            item
            for item in parent_comment_res3["child_comments"]
            if item["id"] == comment.id
        ][0]
        self.assertEqual(comment_from_res2["comment"], "이것은 댓글입니다.")
        self.assertEqual(comment_from_res3["comment"], "[글 작성자와 댓글 작성자만 볼 수 있는 댓글입니다]")
