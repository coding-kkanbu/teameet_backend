from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from kkanbu.operation.models import CommentLike, PostLike
from kkanbu.users.tests.factories import (
    CategoryFactory,
    CommentFactory,
    CommentLikeFactory,
    PostFactory,
    PostLikeFactory,
    UserFactory,
)


class Like_ModelViewSetTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat_topic = CategoryFactory(app="Topic")
        cls.post_topic = PostFactory.create(category=cls.cat_topic)
        cls.comment = CommentFactory.create()

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user2 = UserFactory.create()

        self.client_user1 = APIClient()
        self.client_user1.force_authenticate(user=self.user1)

        self.client_user2 = APIClient()
        self.client_user2.force_authenticate(user=self.user2)

    # PostLikeViewSet unittest
    def test_postlike_get_queryset(self):
        user1_postlikes = PostLikeFactory.create_batch(10, user=self.user1)
        user2_postlikes = PostLikeFactory.create_batch(10, user=self.user2)
        url = reverse("api:PostLike-list")
        res_user1 = self.client_user1.get(url)
        res_user2 = self.client_user2.get(url)

        self.assertEqual(PostLike.objects.count(), 20)
        self.assertEqual(res_user1.status_code, status.HTTP_200_OK)
        self.assertEqual(res_user2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_user1.data["results"]), 10)
        self.assertEqual(len(res_user2.data["results"]), 10)

        for u1_pl in user1_postlikes:
            self.assertNotIn(u1_pl.pk, res_user2.data["results"])
        for u2_pl in user2_postlikes:
            self.assertNotIn(u2_pl.pk, res_user1.data["results"])

    # CommentLikeViewSet unittest
    def test_commentlike_get_queryset(self):
        user1_commentlikes = CommentLikeFactory.create_batch(10, user=self.user1)
        user2_commentlikes = CommentLikeFactory.create_batch(10, user=self.user2)
        url = reverse("api:CommentLike-list")
        res_user1 = self.client_user1.get(url)
        res_user2 = self.client_user2.get(url)

        self.assertEqual(CommentLike.objects.count(), 20)
        self.assertEqual(res_user1.status_code, status.HTTP_200_OK)
        self.assertEqual(res_user2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_user1.data["results"]), 10)
        self.assertEqual(len(res_user2.data["results"]), 10)

        for u1_cl in user1_commentlikes:
            self.assertNotIn(u1_cl.pk, res_user2.data["results"])
        for u2_cl in user2_commentlikes:
            self.assertNotIn(u2_cl.pk, res_user1.data["results"])

    @classmethod
    def tearDownClass(cls):
        cls.cat_topic.delete()
        cls.post_topic.delete()
        cls.comment.delete()
