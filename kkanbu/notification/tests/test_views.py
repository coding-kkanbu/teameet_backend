from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from kkanbu.notification.models import Notification
from kkanbu.notification.serializers import NotificationSerializer
from kkanbu.notification.tests.test_helper import NotificationViewSetTestData


class NotificationViewSetTest(NotificationViewSetTestData):
    def setUp(self):
        self.noti1 = Notification.objects.create(
            notification_type="comment",
            content_object=self.comment1,
            recipient=self.user1,
            message="Got an Comment1",
        )
        self.noti2 = Notification.objects.create(
            notification_type="comment",
            content_object=self.comment2,
            recipient=self.user2,
            message="Got an Comment2",
        )

    def test_notification_list_filter_by_user_success(self):
        """Test notification objects is filtered by user"""
        url = reverse("api:Notification-list")
        user1_res = self.user1_client.get(url)
        self.assertEqual(user1_res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(user1_res.data), 1)
        self.assertTrue("Got an Comment1" in str(user1_res.data))
        self.assertFalse("Got an Comment2" in str(user1_res.data))

        user2_res = self.user2_client.get(url)
        self.assertEqual(user2_res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(user2_res.data), 1)
        self.assertTrue("Got an Comment2" in str(user2_res.data))
        self.assertFalse("Got an Comment1" in str(user2_res.data))

    def test_notification_list_order_by_is_read_success(self):
        """Test notification list ordered by is_read field"""
        for i in range(6):
            Notification.objects.create(
                notification_type="comment",
                content_object=self.comment1,
                recipient=self.user1,
                message=f"Got an Comment_{i}",
            )
        url = reverse("api:Notification-list")
        user1_res1 = self.user1_client.get(url)
        first_instance = user1_res1.data["results"][0]
        noti1 = Notification.objects.get(id=first_instance["id"])
        noti1.is_read = True
        noti1.save()

        user1_res2 = self.user1_client.get(url)
        self.assertNotEqual(user1_res2.data["results"][0]["id"], first_instance["id"])
        self.assertEqual(user1_res2.data["results"][-1]["id"], first_instance["id"])

    def test_notification_retrieve_method_success(self):
        """Test retrieve method affact is_read and successfully redirected"""
        # 처음에 is_read False인지 체크
        self.assertFalse(self.noti2.is_read)
        url = reverse("api:Notification-detail", args=[self.noti2.pk])
        res = self.user2_client.get(url)
        self.assertRedirects(
            res,
            self.noti2.get_absolute_url(),
            status_code=status.HTTP_302_FOUND,
        )
        self.noti2.refresh_from_db()
        self.assertTrue(self.noti2.is_read)

    def test_action_recent_noti_success(self):
        """ "Test custom action work correctly"""
        Notification.objects.all().delete()
        for i in range(10):
            Notification.objects.create(
                notification_type="comment",
                content_object=self.comment1,
                recipient=self.user1,
                message=f"Got an Comment_{i}",
            )
        url = reverse("api:Notification-recent-noti")
        rf = APIRequestFactory()
        request = rf.get("/fake-url/")
        queryset = Notification.objects.order_by("-created")[:5]
        serializer = NotificationSerializer(
            queryset, many=True, context={"request": request}
        )
        res = self.user1_client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print(res.data)
        print(serializer.data)
        self.assertEqual(res.data, serializer.data)
