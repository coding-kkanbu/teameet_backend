import logging

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Category, Comment, Post
from .pagination import PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import BoardListSerializer, PostCreateSerializer, PostSerializer

logger = logging.getLogger(__name__)


# @extend_schema(
#     tags=["post"],
# )
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer


class BoardView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        queryset = Category.objects.order_by("pk")
        serializer = BoardListSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


class PostView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        post_obj = self.get_object()
        serializer = PostSerializer(post_obj)
        return Response(serializer.data)


class TopicView(ListCreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPageNumberPagination

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs["slug"])
        return category.post_set.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


@extend_schema(
    tags=["comment"],
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = PostSerializer
