import logging

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import Comment, Post
from .serializers import PostSerializer

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["post"],
)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@extend_schema(
    tags=["comment"],
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = PostSerializer
