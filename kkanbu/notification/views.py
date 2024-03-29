from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Notification
from .pagination import NotiPageNumberPagination
from .serializers import NotificationSerializer


@extend_schema(
    tags=["notification"],
)
class NotificationViewSet(GenericViewSet, ListModelMixin):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotiPageNumberPagination
    filter_backends = [OrderingFilter]
    ordering = ["is_read", "-created"]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read = True
        instance.save()
        return redirect(instance.get_absolute_url())

    # 네비게이션바 최근 5개 알림사항
    @action(detail=False)
    def recent_noti(self, request):
        queryset = self.get_queryset()
        recent_noti = queryset.order_by("-created")[:5]
        serializer = self.get_serializer(recent_noti, many=True)
        return Response(serializer.data)
