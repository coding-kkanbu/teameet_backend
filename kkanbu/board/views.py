import logging

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView

from .models import Comment, Post
from .serializers import PostCreateSerializer, PostListSerializer

logger = logging.getLogger(__name__)


# @extend_schema(
#     tags=["post"],
# )
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(writer=user)


@extend_schema(
    tags=["comment"],
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = PostListSerializer
