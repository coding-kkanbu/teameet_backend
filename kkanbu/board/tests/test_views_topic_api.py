from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from kkanbu.board.helpers.utils import get_client_ip
from kkanbu.board.models import Category, Post
from kkanbu.board.serializers import PostSerializer
from kkanbu.operation.models import PostBlame, PostLike
from kkanbu.users.tests.factories import CategoryFactory, PostFactory, UserFactory

Topic_URL = reverse("api:Topic-list")


def detail_url(post_id):
    return reverse("api:Topic-detail", args=[post_id])


def sample_post(writer, category, **params):
    defaults = {
        "title": "Test post",
        "content": "Testing post works well",
    }
    defaults.update(params)
    return Post.objects.create(writer=writer, category=category, **defaults)


class PostAPIHTTPMethodsTests(TestCase):
    """Test Http method in post API"""

    def setUp(self):
        self.user = get_user_model().objects.create(
            email="testuser@teameet.com",
            username="test",
            random_name="random name",
            password="testpass1234",
        )
        self.category = Category.objects.create(
            app="Topic", name="테스트토픽", slug="test_topic"
        )

        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.client.force_authenticate(self.user)

    def test_retrieve_post_ordering_by_query(self):
        """Test ordering queryset by query params"""
        # DB 초기화
        Post.objects.all().delete()
        post1 = sample_post(
            writer=self.user, category=self.category, title="Sample Post 1"
        )
        post2 = sample_post(
            writer=self.user, category=self.category, title="Sample Post 2"
        )
        post3 = sample_post(
            writer=self.user, category=self.category, title="Sample Post 3"
        )
        res1 = self.client.get(Topic_URL, {"ordering": "-created"})
        serializer1 = PostSerializer(post1)
        serializer3 = PostSerializer(post3)
        self.assertEqual(res1.data["results"][0], serializer3.data)
        self.assertEqual(res1.data["results"][-1], serializer1.data)

        post2.hit = 25
        post2.save()
        post1.hit = 10
        post1.save()

        res2 = self.client.get(Topic_URL, {"ordering": "-hit"})
        serializer2 = PostSerializer(post2)
        serializer1 = PostSerializer(post1)
        self.assertEqual(res2.data["results"][0], serializer2.data)
        self.assertEqual(res2.data["results"][1], serializer1.data)

    def test_create_post_success(self):
        payload = {
            "title": "My first Posting",
            # PrimaryKeyRelatedField -> NameRelatedField 변경
            "category": self.category.name,
            "content": "This is the first time for my posting.",
            "tags": ["tag1", "tag2"],
        }
        request = self.factory.post(Topic_URL, payload)
        res = self.client.post(Topic_URL, payload, format="json")
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        post = Post.objects.get(id=res.data["id"])
        self.assertEqual(post.title, payload["title"])
        self.assertEqual(post.writer, self.user)
        self.assertEqual(post.ip, get_client_ip(request))

    def test_retrieve_post_success(self):
        post = sample_post(writer=self.user, category=self.category)
        url = detail_url(post.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["hit"], 1)
        self.assertEqual(post.hit, 0)

        post.refresh_from_db()
        self.assertEqual(post.hit, 1)
        res = self.client.get(url)
        self.assertEqual(res.data["hit"], 2)

    def test_delete_post_success(self):
        post = sample_post(writer=self.user, category=self.category)
        url = detail_url(post.id)
        res_del = self.client.delete(url)
        self.assertEqual(res_del.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(post.is_show)
        self.assertIsNone(post.deleted_at)

        post.refresh_from_db()
        self.assertFalse(post.is_show)
        self.assertIsNotNone(post.deleted_at)

        res_get = self.client.get(url)
        self.assertEqual(res_get.status_code, status.HTTP_404_NOT_FOUND)


class PostAPIPermissionTests(TestCase):
    """Test for permission by users' request"""

    def setUp(self):
        self.owner = get_user_model().objects.create(
            email="testuser@teameet.com",
            username="test",
            random_name="random test1",
            password="testpass1234",
        )
        self.user = get_user_model().objects.create(
            email="testuser2@teameet.com",
            username="test2",
            random_name="random test2",
            password="test2pass1234",
        )
        self.category = Category.objects.create(
            app="Topic", name="테스트토픽", slug="test_topic"
        )

        self.client_user = APIClient()
        self.client_user.force_authenticate(self.user)

        self.client_owner = APIClient()
        self.client_owner.force_authenticate(self.owner)

    def test_get_posts_success(self):
        res = self.client_user.get(Topic_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_detail_post_success(self):
        post = sample_post(writer=self.owner, category=self.category)
        url = detail_url(post.id)
        res = self.client_user.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_detail_post_failed_by_user(self):
        post = sample_post(writer=self.owner, category=self.category)
        url = detail_url(post.id)
        res_del = self.client_user.delete(url)
        self.assertEqual(res_del.status_code, status.HTTP_403_FORBIDDEN)
        res_get = self.client_user.get(url)
        self.assertEqual(res_get.status_code, status.HTTP_200_OK)

    def test_patch_detail_post_failed_by_user(self):
        post = sample_post(writer=self.owner, category=self.category)
        url = detail_url(post.id)
        res_pat = self.client_user.patch(url, {"title": "Updated Post Title"})
        self.assertEqual(res_pat.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(post.title, "Test post")

    def test_delete_detail_post_success_by_owner(self):
        post = sample_post(writer=self.owner, category=self.category)
        url = detail_url(post.id)
        res_del = self.client_owner.delete(url)
        self.assertEqual(res_del.status_code, status.HTTP_204_NO_CONTENT)
        res_get = self.client_owner.get(url)
        self.assertEqual(res_get.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_detail_post_success_by_owner(self):
        post = sample_post(writer=self.owner, category=self.category)
        post.tags.add("small talk")
        payload = {"title": "Updated Post Title", "tags": ["Love affair"]}
        url = detail_url(post.id)
        res_pat = self.client_owner.patch(url, payload, format="json")
        self.assertEqual(res_pat.status_code, status.HTTP_200_OK)

        post.refresh_from_db()
        tag_set = post.tags.all()
        self.assertEqual(post.title, payload["title"])
        self.assertEqual(tag_set.filter(name="small talk").count(), 0)
        self.assertEqual(tag_set.filter(name="Love affair").count(), 1)


class TopicAPICustomActionTests(TestCase):
    def setUp(self):
        self.category = CategoryFactory.create(app="Topic")
        self.post = PostFactory.create(category=self.category)
        self.user = UserFactory.create()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_toggle_postlike(self):
        url = reverse("api:Topic-toggle-postlike", args=[self.post.id])
        # attempt 1st when create
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PostLike.objects.filter(post=self.post).exists())
        # post.id가 정확히 들어가는지
        self.assertTrue(PostLike.objects.get(post__id=self.post.id))
        # request user.id가 정확히 들어가는지
        self.assertTrue(PostLike.objects.get(user__id=self.user.id))

        # attempt 2nd when delete
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PostLike.objects.filter(post=self.post).exists())

    def test_report_postblame_once_success(self):
        url = reverse("api:Topic-report-postblame", args=[self.post.id])
        payload = {"reason": "abuse", "description": "blaah blaah"}
        # attempt 1st when create
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PostBlame.objects.filter(post=self.post).exists())
        self.assertTrue(
            PostBlame.objects.filter(
                Q(reason=payload["reason"]) & Q(description=payload["description"])
            ).exists()
        )
        # post.id가 정확히 들어가는지
        self.assertTrue(PostBlame.objects.get(post__id=self.post.id))
        # request user.id가 정확히 들어가는지
        self.assertTrue(PostBlame.objects.get(user__id=self.user.id))

    def test_report_postblame_twice_fail(self):
        url = reverse("api:Topic-report-postblame", args=[self.post.id])
        payload = {"reason": "abuse", "description": "blaah blaah"}
        self.client.post(url, payload)
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data[0].title(), "이미 해당 게시물을 신고했습니다.")

    def test_report_postblame_more_than_blind_count(self):
        users = UserFactory.create_batch(4)
        for user in users:
            PostBlame.objects.create(
                post=self.post,
                user=user,
                reason="abuse",
            )
        self.post.refresh_from_db()
        # 4번째까지는 변화없음
        self.assertTrue(self.post.is_show)
        url = reverse("api:Topic-report-postblame", args=[self.post.id])
        payload = {"reason": "abuse", "description": "blaah blaah"}
        # 5번째 is_show False 확인
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.post.refresh_from_db()
        self.assertFalse(self.post.is_show)
