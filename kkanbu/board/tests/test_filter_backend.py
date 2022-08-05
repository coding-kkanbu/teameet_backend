import random

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from kkanbu.board.serializers import PostSerializer
from kkanbu.users.tests.factories import CategoryFactory, PostFactory, UserFactory


class TagFilterBackendTests(TestCase):
    """Test for tag query in Search API"""

    def setUp(self):
        self.category = CategoryFactory.create(app="Topic")
        self.user = UserFactory.create()
        self.rf = APIRequestFactory()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_func_get_tag_terms(self):
        post1, post2 = PostFactory.create_batch(2, category=self.category)
        post1.tags.add("travel")
        post2.tags.add("travel", "sightseeing")
        tags_payload1 = "travel"
        tags_payload2 = "travel, sightseeing"

        url = reverse("api:Topic-list")
        res1 = self.client.get(url, **{"QUERY_STRING": "tags=" + tags_payload1})
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertIn(PostSerializer(post1).data, res1.data["results"])
        self.assertIn(PostSerializer(post2).data, res1.data["results"])

        res2 = self.client.get(url, **{"QUERY_STRING": "tags=" + tags_payload2})
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertNotIn(PostSerializer(post1).data, res2.data["results"])
        self.assertIn(PostSerializer(post2).data, res2.data["results"])

    def test_filter_queryset(self):
        posts = PostFactory.create_batch(10, category=self.category)
        random_idx = random.sample(range(1, 10), 4)
        pk_list = []
        for i in random_idx:
            posts[i].tags.add("ridi")
            pk_list.append(posts[i].pk)
        for post in posts:
            post.refresh_from_db()
        url = reverse("api:Topic-list")
        res = self.client.get(url, **{"QUERY_STRING": "tags=ridi"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 4)
        for result in res.data["results"]:
            self.assertIn(result["id"], pk_list)
