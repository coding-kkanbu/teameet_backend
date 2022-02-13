import logging

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Category, Comment, Post
from .pagination import PostPageNumberPagination
from .serializers import CategorySerializer, CommentSerializer, PostSerializer

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["post"],
)
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPageNumberPagination

    @action(detail=True)
    def get_comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comment_set
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=["category"],
)
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True)
    def recent_posts(self, request, pk=None):
        category = self.get_object()
        posts = category.post_set.order_by("-created")[:5]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=["comment"],
)
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
