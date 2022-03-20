from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import CommentBlame, CommentLike, PostBlame, PostLike
from .serializers import (
    CommentBlameSerializer,
    CommentLikeSerializer,
    PostBlameSerializer,
    PostLikeSerializer,
)


class PostLikeViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
):
    serializer_class = PostLikeSerializer
    queryset = PostLike.objects.all()


class CommentLikeViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
):
    serializer_class = CommentLikeSerializer
    queryset = CommentLike.objects.all()


class PostBlameViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
):
    serializer_class = PostBlameSerializer
    queryset = PostBlame.objects.all()


class CommentBlameViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
):
    serializer_class = CommentBlameSerializer
    queryset = CommentBlame.objects.all()
