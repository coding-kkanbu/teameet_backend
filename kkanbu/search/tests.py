import random

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from kkanbu.users.tests.factories import PostFactory, UserFactory


class TagFilterBackendTests(TestCase):
    """Test for tag query in Search API"""

    def setUp(self):
        self.user = UserFactory.create()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_filter_queryset(self):
        posts = PostFactory.create_batch(10)
        random_idx = random.sample(range(1, 10), 4)
        pk_list = []
        for i in random_idx:
            posts[i].tags.add("ridi")
            pk_list.append(posts[i].pk)
        for post in posts:
            post.refresh_from_db()
        url = reverse("api:Search-list")
        res = self.client.get(url, **{"QUERY_STRING": "tags=ridi"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 4)
        for result in res.data["results"]:
            self.assertIn(result["id"], pk_list)
