from django.db.models import Q
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from kkanbu.operation.models import CommentBlame, CommentLike
from kkanbu.users.tests.factories import CommentFactory, UserFactory


class CommentAPICustomActionTests(TestCase):
    def setUp(self):
        self.comment = CommentFactory()
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_toggle_commentlike(self):
        url = reverse("api:Comment-toggle-commentlike", args=[self.comment.id])
        # attempt 1st when create
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CommentLike.objects.filter(comment=self.comment).exists())
        # comment.id가 정확히 들어가는지
        self.assertTrue(CommentLike.objects.get(comment__id=self.comment.id))
        # request user.id가 정확히 들어가는지
        self.assertTrue(CommentLike.objects.get(user__id=self.user.id))

        # attempt 2nd when delete
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CommentLike.objects.filter(comment=self.comment).exists())

    def test_report_commentblame_once_success(self):
        url = reverse("api:Comment-report-commentblame", args=[self.comment.id])
        payload = {"reason": "abuse", "description": "blaah blaah"}
        # attempt 1st when create
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CommentBlame.objects.filter(comment=self.comment).exists())
        self.assertTrue(
            CommentBlame.objects.filter(
                Q(reason=payload["reason"]) & Q(description=payload["description"])
            ).exists()
        )
        # comment.id가 정확히 들어가는지
        self.assertTrue(CommentBlame.objects.get(comment__id=self.comment.id))
        # request user.id가 정확히 들어가는지
        self.assertTrue(CommentBlame.objects.get(user__id=self.user.id))

    def test_report_commentblame_twice_fail(self):
        url = reverse("api:Comment-report-commentblame", args=[self.comment.id])
        payload = {"reason": "abuse", "description": "blaah blaah"}
        self.client.post(url, payload)
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data[0].title(), "이미 해당 댓글을 신고했습니다.")

    def test_report_postblame_more_than_blind_count(self):
        users = UserFactory.create_batch(2)
        for user in users:
            CommentBlame.objects.create(
                comment=self.comment,
                user=user,
                reason="abuse",
            )
        self.comment.refresh_from_db()
        # 2번째까지는 변화없음
        self.assertTrue(self.comment.is_show)
        url = reverse("api:Comment-report-commentblame", args=[self.comment.id])
        payload = {"reason": "abuse", "description": "blaah blaah"}
        # 3번째 is_show False 확인
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.comment.refresh_from_db()
        self.assertFalse(self.comment.is_show)
