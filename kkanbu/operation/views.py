from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet

from kkanbu.users.models import User

from .models import CommentBlame, CommentLike, PostBlame, PostLike
from .serializers import (
    CommentBlameSerializer,
    CommentLikeSerializer,
    PostBlameSerializer,
    PostLikeSerializer,
)


@extend_schema(tags=["operation"])
class PostLikeViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
):
    serializer_class = PostLikeSerializer
    queryset = PostLike.objects.all()

    def get_queryset(self):
        assert isinstance(self.request.user, User)
        return self.queryset.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return redirect(instance.get_absolute_url())


@extend_schema(tags=["operation"])
class CommentLikeViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
):
    serializer_class = CommentLikeSerializer
    queryset = CommentLike.objects.all()

    def get_queryset(self):
        assert isinstance(self.request.user, User)
        return self.queryset.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return redirect(instance.get_absolute_url())


@extend_schema(tags=["operation"])
class PostBlameViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
):
    serializer_class = PostBlameSerializer
    queryset = PostBlame.objects.all()
    permission_classes = [IsAdminUser]


@extend_schema(tags=["operation"])
class CommentBlameViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
):
    serializer_class = CommentBlameSerializer
    queryset = CommentBlame.objects.all()
    permission_classes = [IsAdminUser]
