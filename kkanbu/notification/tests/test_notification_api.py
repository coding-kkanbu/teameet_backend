from django.urls import reverse
from rest_framework import status

from kkanbu.notification.models import Notification
from kkanbu.notification.tests.test_api_helper import NotificationViewSetTestData


class NotificationViewSetTest(NotificationViewSetTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        Notification.objects.create(
            notification_type="comment",
            sender=cls.comment1,
            recipient=cls.user1,
            message="Got an Comment1",
        )
        Notification.objects.create(
            notification_type="comment",
            sender=cls.comment2,
            recipient=cls.user2,
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
                sender=self.comment1,
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
