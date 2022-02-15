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

    @action(detail=True, methods=["POST"])
    def toggle_postlike(self, request, pk=None):
        post = self.get_object()
        post_likes = post.postlike_set
        user = request.user

        post_like = post_likes.filter(user=user)
        # check if post has postlike from the user
        if post_like:
            # delete post like if already liked by the user
            post_like.delete()
            serializer = self.get_serializer(post, many=False)
            return Response(serializer.data)
        else:
            # create post like if not liked by the user
            post.postlike_set.create(user=user)
            serializer = self.get_serializer(post, many=False)
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

    @action(detail=True, methods=["POST"])
    def toggle_commentlike(self, request, pk=None):
        comment = self.get_object()
        comment_likes = comment.postlike_set
        user = request.user

        comment_like = comment_likes.filter(user=user)
        # check if comment has commentlike from the user
        if comment_like:
            # delete comment like if already liked by the user
            comment_like.delete()
            serializer = self.get_serializer(comment, many=False)
            return Response(serializer.data)
        else:
            # create comment like if not liked by the user
            comment.postlike_set.create(user=user)
            serializer = self.get_serializer(comment, many=False)
            return Response(serializer.data)
