from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from kkanbu.board.models import Comment, Post

from .models import CommentBlame, CommentLike, PostBlame, PostLike


class PostIndexSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content"]


class CommentIndexSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "comment"]


class PostLikeSerializer(ModelSerializer):
    post = PostIndexSerializer()

    class Meta:
        model = PostLike
        fields = ["id", "post", "user", "created"]

        validators = [
            UniqueTogetherValidator(
                queryset=PostLike.objects.all(), fields=["post", "user"]
            )
        ]


class PostBlameSerializer(ModelSerializer):
    post = PostIndexSerializer()

    class Meta:
        model = PostBlame
        fields = "__all__"

        validators = [
            UniqueTogetherValidator(
                queryset=PostBlame.objects.all(),
                fields=["post", "user"],
                message="이미 해당 게시물을 신고했습니다.",
            )
        ]


class CommentLikeSerializer(ModelSerializer):
    comment = CommentIndexSerializer()

    class Meta:
        model = CommentLike
        fields = ["id", "comment", "user", "created"]

        validators = [
            UniqueTogetherValidator(
                queryset=CommentLike.objects.all(), fields=["comment", "user"]
            )
        ]


class CommentBlameSerializer(ModelSerializer):
    comment = CommentIndexSerializer()

    class Meta:
        model = CommentBlame
        fields = "__all__"

        validators = [
            UniqueTogetherValidator(
                queryset=CommentBlame.objects.all(),
                fields=["comment", "user"],
                message="이미 해당 댓글을 신고했습니다.",
            )
        ]
