from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from kkanbu.operation.models import CommentBlame, CommentLike, PostBlame, PostLike
from kkanbu.operation.serializers import (
    CommentBlameSerializer,
    CommentLikeSerializer,
    PostBlameSerializer,
    PostLikeSerializer,
)
from kkanbu.users.tests.factories import (
    CategoryFactory,
    CommentFactory,
    PostFactory,
    UserFactory,
)


class LikeSerializerTests(TestCase):
    def setUp(self):
        self.category = CategoryFactory.create(app="Topic")
        self.post = PostFactory.create(category=self.category)
        self.comment = CommentFactory.create(post=self.post)
        self.user = UserFactory.create()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_postlike_delete_duplicate(self):
        PostLike.objects.create(
            post=self.post,
            user=self.user,
        )
        self.assertTrue(
            PostLike.objects.filter(post=self.post, user=self.user).exists()
        )
        serializer = PostLikeSerializer(data={})
        serializer.is_valid()
        serializer.save(post=self.post, user=self.user)
        self.assertFalse(
            PostLike.objects.filter(post=self.post, user=self.user).exists()
        )

    def test_commentlike_delete_duplicate(self):
        CommentLike.objects.create(
            comment=self.comment,
            user=self.user,
        )
        self.assertTrue(
            CommentLike.objects.filter(comment=self.comment, user=self.user).exists()
        )
        serializer = CommentLikeSerializer(data={})
        serializer.is_valid()
        serializer.save(comment=self.comment, user=self.user)
        self.assertFalse(
            CommentLike.objects.filter(comment=self.comment, user=self.user).exists()
        )


class BlameSerializerTests(TestCase):
    def setUp(self):
        self.category = CategoryFactory.create(app="Topic")
        self.post = PostFactory.create(category=self.category)
        self.comment = CommentFactory.create(post=self.post)
        self.user = UserFactory.create()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_postblame_validation_error(self):
        PostBlame.objects.create(
            post=self.post,
            user=self.user,
            reason="falsefact",
            description="blaah blaah",
        )
        payload = {"reason": "abuse", "description": "abuse hardly"}
        serializer = PostBlameSerializer(data=payload)
        serializer.is_valid()
        with self.assertRaises(ValidationError):
            serializer.save(post=self.post, user=self.user)

    def test_commentblame_validation_error(self):
        CommentBlame.objects.create(
            comment=self.comment,
            user=self.user,
            reason="falsefact",
            description="blaah blaah",
        )
        payload = {"reason": "abuse", "description": "abuse hardly"}
        serializer = CommentBlameSerializer(data=payload)
        serializer.is_valid()
        with self.assertRaises(ValidationError):
            serializer.save(comment=self.comment, user=self.user)
