from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import CommentBlame, PostBlame
from .serializers import CommentBlameSerializer, PostBlameSerializer


class PostBlameViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = PostBlameSerializer
    queryset = PostBlame.objects.all()


class CommentBlameViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = CommentBlameSerializer
    queryset = CommentBlame.objects.all()
