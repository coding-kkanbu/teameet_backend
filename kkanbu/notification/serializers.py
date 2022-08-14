from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
)

from .models import Notification


class NotificationSerializer(ModelSerializer):
    sender_info = SerializerMethodField()
    url = HyperlinkedIdentityField(view_name="api:Notification-detail")

    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "sender_info",
            "message",
            "is_read",
            "created",
            "url",
        ]

    def get_sender_info(self, obj):
        if obj.notification_type == "comment":
            sender_info = obj.content_object.writer.username
        else:
            sender_info = obj.content_object.user.username
        return sender_info
