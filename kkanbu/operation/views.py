from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from .models import CommentBlame, PostBlame
from .serializers import CommentBlameSerializer, PostBlameSerializer


class PostBlameViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = PostBlameSerializer
    queryset = PostBlame.objects.all()


class CommentBlameViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = CommentBlameSerializer
    queryset = CommentBlame.objects.all()
