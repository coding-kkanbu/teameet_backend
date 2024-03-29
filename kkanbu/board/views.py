import logging

from django.conf import settings
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from kkanbu.notification.signals import notify
from kkanbu.operation.serializers import (
    CommentBlameSerializer,
    CommentLikeSerializer,
    PostBlameSerializer,
    PostLikeSerializer,
)

from .helpers.filters import PostOrderingFilter, TagFilter
from .helpers.pagination import CategoryPageNumberPagination, PostPageNumberPagination
from .helpers.permissions import IsOwnerOrReadOnly
from .helpers.utils import get_client_ip
from .models import Category, Comment, Post
from .serializers import (
    CategorySerializer,
    CommentListSerializer,
    CommentSerializer,
    PitAPatSerializer,
    PostListSerializer,
    PostSerializer,
)

logger = logging.getLogger(__name__)


class AbstractPostViewSet(ModelViewSet):
    """Post Model을 기반으로 한 객체를 다루는 필요한 공통 속성만 뽑아낸 ViewSet"""

    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, PostOrderingFilter, TagFilter]
    pagination_class = PostPageNumberPagination
    search_fields = ["title", "content"]

    def get_serializer_class(self):
        if self.action == "toggle_postlike":
            return PostLikeSerializer
        if self.action == "report_postblame":
            return PostBlameSerializer
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.hit += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        client_ip = get_client_ip(self.request)
        serializer.save(writer=self.request.user, ip=client_ip)

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
        comment_set = post.comment_set.filter(
            is_show=True, parent_comment=None
        ).order_by("created")
        serializer = CommentSerializer(
            comment_set, context={"request": request, "post": post}, many=True
        )
        return Response(serializer.data)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def toggle_postlike(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        postlike = serializer.save(post=post, user=request.user)
        if postlike:
            notify.send(
                notification_type="postlike",
                sender=postlike,
                recipient=post.writer,
                message="회원님의 게시글을 좋아합니다.",
            )
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def report_postblame(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        postblame = serializer.save(post=post, user=request.user)
        # TODO 게시글신고 상수 규칙 변경
        # 신고 5회 이상이면 게시글 블라인드 처리
        if postblame:
            if post.postblame_set.count() >= settings.POSTBLAME_AUTO_BLIND_COUNT:
                post.is_show = False
                post.save()
                # 알림 signal 발송
                notify.send(
                    notification_type="postblame",
                    sender=postblame,
                    recipient=post.writer,
                    message="회원님의 게시물이 신고 횟수 초과로 블라인드 처리되었습니다.",
                )
            return Response(
                {"message": "회원님의 신고가 접수되었습니다."},
                status=status.HTTP_201_CREATED,
            )


@extend_schema(
    tags=["topic"],
)
class TopicViewSet(AbstractPostViewSet):
    """Post 모델로 '토픽' 게시물을 만드는데 사용되는 ViewSet"""

    queryset = Post.objects.filter(is_show=True, category__app="Topic")
    serializer_class = PostSerializer


@extend_schema(
    tags=["pitapat"],
)
class PitAPatViewSet(AbstractPostViewSet):
    """Post 모델로 '두근두근' 게시물을 만드는데 사용되는 ViewSet"""

    queryset = Post.objects.filter(is_show=True, category__app="PitAPat")
    serializer_class = PitAPatSerializer

    # TODO connected 선택할 때 다시 되돌릴 수 없다 팝업창 추가
    @action(detail=True, methods=["PATCH"])
    def connected(self, request, pk=None):
        post = self.get_object()
        setattr(post.sogaetingoption, "connected", True)
        post.sogaetingoption.save()
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sogaetingoption.connected:
            return Response(status=status.HTTP_204_NO_CONTENT)
        instance.hit += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(
    tags=["category"],
)
class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    pagination_class = CategoryPageNumberPagination
    lookup_field = "slug"
    ordering = PostOrderingFilter.ordering

    def get_serializer_class(self):
        if self.action == "list":
            return CategorySerializer
        else:
            return PostListSerializer

    @action(detail=True)
    def recent_posts(self, request, slug=None):
        category = self.get_object()
        queryset = category.post_set.filter(is_show=True).order_by("-created")[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(app="Topic")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = instance.post_set.filter(is_show=True)
        filtered_queryset = PostOrderingFilter().filter_queryset(
            request, queryset, self
        )

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=["comment"],
)
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(is_show=True)

    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return CommentListSerializer
        elif self.action == "report_commentblame":
            return CommentBlameSerializer
        elif self.action == "toggle_commentlike":
            return CommentLikeSerializer
        return self.serializer_class

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

    def perform_destroy(self, instance):
        instance.is_show = False
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def toggle_commentlike(self, request, pk=None):
        comment = self.get_object()
        seriaizer = self.get_serializer(data=request.data)
        seriaizer.is_valid(raise_exception=True)
        commentlike = seriaizer.save(comment=comment, user=request.user)
        if commentlike:
            notify.send(
                notification_type="commentlike",
                sender=commentlike,
                recipient=comment.writer,
                message="회원님의 댓글을 좋아합니다.",
            )
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def report_commentblame(self, request, pk=None):
        comment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        commentblame = serializer.save(comment=comment, user=request.user)
        # TODO 댓글신고 상수 규칙 변경
        # 신고 3회 이상이면 댓글 블라인드 처리
        if commentblame:
            if (
                comment.commentblame_set.count()
                >= settings.COMMENTBLAME_AUTO_BLIND_COUNT
            ):
                comment.is_show = False
                comment.save()
                notify.send(
                    notification_type="commentblame",
                    sender=commentblame,
                    recipient=comment.writer,
                    message="회원님의 댓글이 신고 횟수 초과로 블라인드 처리되었습니다.",
                )
            return Response(
                {"message": "회원님의 신고가 접수되었습니다."}, status=status.HTTP_201_CREATED
            )
