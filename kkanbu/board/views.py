import logging

from django.conf import settings
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from kkanbu.notification.signals import notify

from .helpers.pitapat import PitAPatDetailSerializer, PitAPatListSerializer
from .helpers.utils import UniqueBlameError, get_client_ip
from .models import Category, Comment, Post, SogaetingOption
from .pagination import CategoryPageNumberPagination, PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    PostDetailSerializer,
    PostListSerializer,
)

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["post"],
)
class PostViewSet(ModelViewSet):
    serializer_class = PostListSerializer
    detail_serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PostPageNumberPagination

    def get_queryset(self):
        # TODO 최신순/인기순 정렬 방법 추가
        return (
            Post.objects.select_related("sogaetingoption")
            .exclude(sogaetingoption__isnull=False)
            .filter(is_show=True)
            .order_by("-created")
        )

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "update":
            if hasattr(self, "detail_serializer_class"):
                return self.detail_serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        client_ip = get_client_ip(self.request)
        serializer.save(writer=self.request.user, ip=client_ip)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.hit += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        client_ip = get_client_ip(self.request)
        serializer.save(ip=client_ip)

    def perform_destroy(self, instance):
        instance.is_show = False
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=True, permission_classes=[IsAuthenticated])
    def get_comments(self, request, pk=None):
        post = self.get_object()
        comment_set = post.comment_set.order_by("created")
        for comment in comment_set:
            if comment.secret:
                if comment.parent_comment:
                    if (
                        request.user != comment.writer
                        and request.user != comment.parent_comment.writer
                        and request.user != post.writer
                    ):
                        comment.comment = "[글 작성자와 댓글 작성자만 볼 수 있는 댓글입니다]"
                else:
                    if request.user != comment.writer and request.user != post.writer:
                        comment.comment = "[글 작성자와 댓글 작성자만 볼 수 있는 댓글입니다]"
        serializer = CommentSerializer(comment_set, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def toggle_postlike(self, request, pk=None):
        post = self.get_object()
        post_likes = post.postlike_set
        user = request.user

        post_like = post_likes.filter(user=user)
        # check if post has postlike from the user
        if post_like:
            # delete post like if already liked by the user
            post_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # create post like if not liked by the user
            instance = post_likes.create(user=user)
            notify.send(
                notification_type="postlike",
                sender=instance,
                recipient=post.writer,
                message="회원님의 게시글을 좋아합니다.",
            )
            return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def toggle_postblame(self, request, pk=None):
        post = self.get_object()
        postblame_set = post.postblame_set
        user = request.user

        # 이미 신고를 했으면 다시 불가능
        postblame = postblame_set.filter(user=user)
        if postblame:
            raise UniqueBlameError
        # 신고를 안했으면 한 번 가능
        # TODO '정말로 신고하시겠습니까?' 팝업 메세지 창 추가
        else:
            instance = postblame_set.create(user=user)
            # TODO 게시글신고 상수 규칙 추가
            # 신고 5회 이상이면 게시글 블라인드 처리
            if postblame_set.count() >= settings.POSTBLAME_AUTO_BLIND_COUNT:
                post.is_show = False
                post.save()

                notify.send(
                    notification_type="postblame",
                    sender=instance,
                    recipient=post.writer,
                    message="회원님의 게시물이 신고 횟수 초과로 블라인드 처리되었습니다.",
                )
            return Response(status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["category"],
)
class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPageNumberPagination

    @action(detail=False)
    def topic(self, request):
        queryset = self.get_queryset().filter(app="Topic")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def pitapat(self, request):
        queryset = self.get_queryset().filter(app="PitAPat")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.app == "Topic":
            retrieve_serializer = PostListSerializer
        if instance.app == "PitAPat":
            retrieve_serializer = PitAPatListSerializer
        queryset = instance.post_set.filter(is_show=True).order_by("-created")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = retrieve_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = retrieve_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=["comment"],
)
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(parent_comment=None)

    def perform_create(self, serializer):
        client_ip = get_client_ip(self.request)
        instance = serializer.save(writer=self.request.user, ip=client_ip)
        if instance.parent_comment:
            notify.send(
                notification_type="comment",
                sender=instance,
                recipient=instance.parent_comment.writer,
                message="내 댓글에 답글이 달렸습니다.",
            )
        else:
            notify.send(
                notification_type="comment",
                sender=instance,
                recipient=instance.post.writer,
                message="내 게시글에 댓글이 달렸습니다.",
            )

    def perform_update(self, serializer):
        client_ip = get_client_ip(self.request)
        serializer.save(ip=client_ip)

    def perform_destroy(self, instance):
        instance.is_show = False
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def toggle_commentlike(self, request, pk=None):
        comment = self.get_object()
        comment_likes = comment.commentlike_set
        user = request.user

        comment_like = comment_likes.filter(user=user)
        # check if comment has commentlike from the user
        if comment_like:
            # delete comment like if already liked by the user
            comment_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # create comment like if not liked by the user
            instance = comment_likes.create(user=user)
            notify.send(
                notification_type="commentlike",
                sender=instance,
                recipient=comment.writer,
                message="회원님의 댓글을 좋아합니다.",
            )
            return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def toggle_commentblame(self, request, pk=None):
        comment = self.get_object()
        commentblame_set = comment.commentblame_set
        user = request.user

        commentblame = commentblame_set.filter(user=user)
        if commentblame:
            raise UniqueBlameError
        else:
            # TODO '정말로 신고하시겠습니까?' 팝업 메세지 창 추가
            instance = commentblame_set.create(user=user)
            # TODO 댓글신고 상수 규칙 추가
            # 신고 3회 이상이면 댓글 블라인드 처리
            if commentblame_set.count() >= settings.COMMENTBLAME_AUTO_BLIND_COUNT:
                comment.is_show = False
                comment.save()

                notify.send(
                    notification_type="commentblame",
                    sender=instance,
                    recipient=comment.writer,
                    message="회원님의 댓글이 신고 횟수 초과로 블라인드 처리되었습니다.",
                )
            return Response(status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["sogaetingoption"],
)
class PitAPatViewSet(PostViewSet):
    serializer_class = PitAPatListSerializer
    detail_serializer_class = PitAPatDetailSerializer

    def get_queryset(self):
        return (
            Post.objects.select_related("sogaetingoption")
            .exclude(sogaetingoption__isnull=True)
            .filter(is_show=True)
            .order_by("-created")
        )

    def post_create(self, request, **validated_data):
        writer = request.user
        client_ip = get_client_ip(request)
        post = Post.objects.create(
            category=validated_data.get("category"),
            title=validated_data.get("title"),
            content=validated_data.get("content"),
            writer=writer,
            ip=client_ip,
        )
        return post

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = self.post_create(request, **serializer.validated_data)
        serializer.validated_data["post_id"] = post.id
        SogaetingOption.objects.create(
            post=post,
            region=serializer.validated_data.get("sogaetingoption")["region"],
            gender=serializer.validated_data.get("sogaetingoption")["gender"],
            age=serializer.validated_data.get("sogaetingoption")["age"],
        )
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
