from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from .models import CommentBlame, CommentLike, PostBlame, PostLike


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = PostLike
        field = "__all__"

        validators = [
            UniqueTogetherValidator(
                queryset=PostLike.objects.all(), fields=["post", "user"]
            )
        ]


class PostBlameSerializer(ModelSerializer):
    class Meta:
        model = PostBlame
        fields = ["post", "user"]

        validators = [
            UniqueTogetherValidator(
                queryset=PostBlame.objects.all(),
                fields=["post", "user"],
                message="이미 해당 게시물을 신고했습니다.",
            )
        ]


class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = "__all__"

        validators = [
            UniqueTogetherValidator(
                queryset=CommentLike.objects.all(), fields=["comment", "user"]
            )
        ]


class CommentBlameSerializer(ModelSerializer):
    class Meta:
        model = CommentBlame
        fields = ["comment", "user"]

        validators = [
            UniqueTogetherValidator(
                queryset=CommentBlame.objects.all(),
                fields=["comment", "user"],
                message="이미 해당 댓글을 신고했습니다.",
            )
        ]
