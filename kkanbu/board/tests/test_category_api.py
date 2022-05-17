from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from kkanbu.board.models import Category, Post
from kkanbu.board.utils import url_with_query

CATEGORY_LIST_URL = reverse("api:category-list")
CATEGORY_DETAIL_URL = reverse("api:category-detail", args=["test1"])


class CategoryViewSetAPITest(APITestCase):
    """Test Category API"""

    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(
            email="ridi@teameet.com",
            nickname="ridi",
            username="ridi",
            password="ridipass12",
        )
        cat = Category.objects.create(app="Topic", name="테스트1", slug="test1")
        for idx in range(15):
            Post.objects.create(
                category=cat,
                writer=user,
                title=f"Post_{idx}",
                content=f"Post_{idx}_content",
            )

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="test@test.com",
            nickname="test12",
            username="test12",
            password="testpass12",
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_category_success(self):
        """Test user allowed GET method & received appropriate data"""
        res = self.client.get(CATEGORY_DETAIL_URL)
        res_page2 = self.client.get(url_with_query(CATEGORY_DETAIL_URL, page=2))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"][0]["title"], "Post_0")
        self.assertEqual(res.data["results"][9]["content"], "Post_9_content")
        self.assertEqual(res_page2.data["results"][-1]["title"], "Post_14")

    def test_create_category_not_allowed(self):
        """Test user not allowed POST method"""
        payload = {"app": "Topic", "name": "테스트2", "slug": "test2"}
        res = self.client.post(CATEGORY_LIST_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_category_not_allowed(self):
        """Test user not allowed UPDATE method"""
        payload = {"name": "테스트2", "slug": "test2"}
        res_1 = self.client.put(CATEGORY_DETAIL_URL, payload, format="json")
        res_2 = self.client.patch(CATEGORY_DETAIL_URL, payload, format="json")
        self.assertEqual(res_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(res_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_category_not_allowed(self):
        """Test user not allowed DELETE method"""
        res = self.client.delete(CATEGORY_DETAIL_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_recent_posts_GET_five_object(self):
        """Test custom recent posts method only got 5 objects"""
        url = reverse("api:category-recent-posts", args=["test1"])
        res = self.client.get(url)
        self.assertEqual(len(res.data), 5)

    def test_is_show_filter(self):
        """Test only get posts if is_show is True"""
        post = Post.objects.order_by("-created")[0]
        post.is_show = False
        post.save()
        url = reverse("api:category-recent-posts", args=["test1"])
        res_1 = self.client.get(url)
        self.assertTrue(post.title not in res_1.data)
        self.assertTrue(post.content not in res_1.data)

        res_2 = self.client.get(CATEGORY_DETAIL_URL)
        self.assertTrue(post.title not in res_2.data)
        self.assertTrue(post.content not in res_2.data)

        res_3 = self.client.get(url_with_query(CATEGORY_DETAIL_URL, page=2))
        self.assertTrue(post.title not in res_3.data)
        self.assertTrue(post.content not in res_3.data)

    def test_pagination_is_ten(self):
        res = self.client.get(CATEGORY_DETAIL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 10)

    def test_lists_all_post_object_per_category(self):
        """Get second page and confirm it has (exactly) remaining 5 items"""
        res = self.client.get(url_with_query(CATEGORY_DETAIL_URL, page=2))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 5)
