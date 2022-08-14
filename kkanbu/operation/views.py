from drf_spectacular.utils import extend_schema
from rest_framework.mixins import ListModelMixin
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
):
    serializer_class = PostLikeSerializer
    queryset = PostLike.objects.all()

    def get_queryset(self):
        assert isinstance(self.request.user, User)
        return self.queryset.filter(user=self.request.user)


@extend_schema(tags=["operation"])
class CommentLikeViewSet(
    GenericViewSet,
    ListModelMixin,
):
    serializer_class = CommentLikeSerializer
    queryset = CommentLike.objects.all()

    def get_queryset(self):
        assert isinstance(self.request.user, User)
        return self.queryset.filter(user=self.request.user)


@extend_schema(tags=["operation"])
class PostBlameViewSet(
    GenericViewSet,
    ListModelMixin,
):
    serializer_class = PostBlameSerializer
    queryset = PostBlame.objects.all()
    permission_classes = [IsAdminUser]


@extend_schema(tags=["operation"])
class CommentBlameViewSet(
    GenericViewSet,
    ListModelMixin,
):
    serializer_class = CommentBlameSerializer
    queryset = CommentBlame.objects.all()
    permission_classes = [IsAdminUser]
