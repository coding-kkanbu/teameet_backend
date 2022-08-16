from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from kkanbu.board.serializers import PostListSerializer
from kkanbu.users.utils import generate_random_name

from .serializers import UserProfileSerializer, UserSerializer

User = get_user_model()


@extend_schema(
    tags=["users"],
)
class UserViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    lookup_url_kwarg = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == "upload_image":
            return UserProfileSerializer
        else:
            return self.serializer_class

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True)
    def my_posts(self, request, username=None):
        user = self.get_object()
        user_posts = user.post_set.filter(is_show=True).order_by("-created")

        page = self.paginate_queryset(user_posts)
        if page is not None:
            serializer = PostListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostListSerializer(user_posts, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, methods=["POST"])
    def set_random_name(self, request, username=None):
        user = self.get_object()
        random_name = generate_random_name()
        user.random_name = random_name
        user.save()
        serializer = self.get_serializer(user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, methods=["GET", "POST"], url_path="upload_image")
    def upload_image(self, request, username=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
