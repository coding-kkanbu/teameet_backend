from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(GenericViewSet, ListModelMixin):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user_to=self.request.user)
