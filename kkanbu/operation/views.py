from drf_spectacular.utils import extend_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

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
    CreateModelMixin,
    ListModelMixin,
):
    serializer_class = PostLikeSerializer
    queryset = PostLike.objects.all()


@extend_schema(tags=["operation"])
class CommentLikeViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
):
    serializer_class = CommentLikeSerializer
    queryset = CommentLike.objects.all()


@extend_schema(tags=["operation"])
class PostBlameViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
):
    serializer_class = PostBlameSerializer
    queryset = PostBlame.objects.all()


@extend_schema(tags=["operation"])
class CommentBlameViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
):
    serializer_class = CommentBlameSerializer
    queryset = CommentBlame.objects.all()
