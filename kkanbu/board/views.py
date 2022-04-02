import logging

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from kkanbu.notification.signals import notify

from .models import Category, Comment, Post
from .pagination import PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import CategorySerializer, CommentSerializer, PostSerializer
from .utils import UniqueBlameError, get_client_ip

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["post"],
)
class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PostPageNumberPagination

    def get_queryset(self):
        return Post.objects.filter(is_show=True)

    def perform_create(self, serializer):
        client_ip = get_client_ip(self.request)
        serializer.save(writer=self.request.user, ip=client_ip)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.hit += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.is_show = False
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=True)
    def get_comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comment_set
        serializer = CommentSerializer(comments, many=True)
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

    @action(detail=True, methods=["POST", "PUT"], permission_classes=[IsAuthenticated])
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
            # 신고 5회 이상이면 게시글 블라인드 처리
            if postblame_set.count() >= 5:
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
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(is_show=True)

    def perform_create(self, serializer):
        client_ip = get_client_ip(self.request)
        instance = serializer.save(writer=self.request.user, ip=client_ip)
        notify.send(
            notification_type="comment",
            sender=instance,
            recipient=instance.post.writer,
            message="게시글에 댓글이 달렸습니다.",
        )

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

    @action(detail=True, methods=["POST", "PUT"], permission_classes=[IsAuthenticated])
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
            # 신고 3회 이상이면 댓글 블라인드 처리
            if commentblame_set.count() >= 3:
                comment.is_show = False
                comment.save()

                notify.send(
                    notification_type="commentblame",
                    sender=instance,
                    recipient=comment.writer,
                    message="회원님의 댓글이 신고 횟수 초과로 블라인드 처리되었습니다.",
                )
            return Response(status=status.HTTP_201_CREATED)
