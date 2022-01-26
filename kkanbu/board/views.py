import logging

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from .models import Category, Comment
from .serializers import BoardListSerializer, PostSerializer

logger = logging.getLogger(__name__)


# @extend_schema(
#     tags=["post"],
# )
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer


class BoardListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = BoardListSerializer


@extend_schema(
    tags=["comment"],
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = PostSerializer
