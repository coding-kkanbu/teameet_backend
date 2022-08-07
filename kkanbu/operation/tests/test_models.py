from django.db import IntegrityError
from django.test import TestCase

from kkanbu.operation.models import CommentLike, PostLike
from kkanbu.users.tests.factories import (
    CategoryFactory,
    CommentFactory,
    PostFactory,
    UserFactory,
)


class Like_ModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat_topic = CategoryFactory(app="Topic")
        cls.cat_pitapat = CategoryFactory(app="PitAPat")
        cls.user = UserFactory.create()
        cls.post_topic = PostFactory.create(category=cls.cat_topic)
        cls.post_pitapat = PostFactory.create(category=cls.cat_pitapat)
        cls.comment = CommentFactory.create()

    def setUp(self):
        self.topic_like = PostLike.objects.create(
            post=self.post_topic,
            user=self.user,
        )
        self.pitapat_like = PostLike.objects.create(
            post=self.post_pitapat,
            user=self.user,
        )
        self.comment_like = CommentLike.objects.create(
            comment=self.comment,
            user=self.user,
        )

    # PostLike Model TEST
    def test_postlike_get_absolute_url(self):
        self.assertEqual(
            self.topic_like.get_absolute_url(),
            f"/api/v1/topic/{self.post_topic.pk}/",
        )
        self.assertEqual(
            self.pitapat_like.get_absolute_url(),
            f"/api/v1/pitapat/{self.post_pitapat.pk}/",
        )

    def test_postlike_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            postlike_invalid = PostLike(post=self.post_topic, user=self.user)
            postlike_invalid.save()

    # CommentLike Model TEST
    def test_commentlike_get_absolute_url(self):
        self.assertEqual(
            self.comment_like.get_absolute_url(),
            f"/api/v1/comment/{self.comment.pk}/",
        )

    def test_commentlike_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            commentlike_invalid = CommentLike(comment=self.comment, user=self.user)
            commentlike_invalid.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.post_topic.delete()
        cls.post_pitapat.delete()
        cls.comment.delete()
