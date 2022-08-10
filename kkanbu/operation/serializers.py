from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)
from rest_framework.validators import UniqueTogetherValidator

from kkanbu.users.api.serializers import UserInfoSerializer

from .models import CommentBlame, CommentLike, PostBlame, PostLike

User = get_user_model()


class PostLikeSerializer(ModelSerializer):
    post = StringRelatedField()
    url = SerializerMethodField()

    class Meta:
        model = PostLike
        fields = ["id", "post", "created", "url"]
        validators = [
            UniqueTogetherValidator(
                queryset=PostLike.objects.all(), fields=["post", "user"]
            )
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())


class CommentLikeSerializer(ModelSerializer):
    comment = StringRelatedField()
    url = SerializerMethodField()

    class Meta:
        model = CommentLike
        fields = ["id", "comment", "created", "url"]

        validators = [
            UniqueTogetherValidator(
                queryset=CommentLike.objects.all(), fields=["comment", "user"]
            )
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())


class PostBlameSerializer(ModelSerializer):
    post_title = SerializerMethodField()
    user_info = SerializerMethodField()
    url = SerializerMethodField()

    class Meta:
        model = PostBlame
        fields = [
            "id",
            "post",
            "post_title",
            "user",
            "user_info",
            "reason",
            "description",
            "created",
            "url",
        ]

        validators = [
            UniqueTogetherValidator(
                queryset=PostBlame.objects.all(),
                fields=["post", "user"],
                message="이미 해당 댓글을 신고했습니다.",
            )
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())

    def get_post_title(self, obj):
        return obj.post.title

    def get_user_info(self, obj):
        user = User.objects.get(id=obj.user.id)
        return UserInfoSerializer(user).data

    def save(self):
        post_id = self.validated_data["post"].id
        user_id = self.validated_data["user"].id
        if post_id != self.context.get("post_id"):
            raise ValidationError("신고된 게시물 id가 일치하지 않습니다.")
        if user_id != self.context.get("request").user.id:
            raise ValidationError("신고한 유저의 id와 일치하지 않습니다.")
        return super().save()


class CommentBlameSerializer(ModelSerializer):
    content = SerializerMethodField()
    user_info = SerializerMethodField()
    url = SerializerMethodField()

    class Meta:
        model = CommentBlame
        fields = [
            "id",
            "comment",
            "content",
            "user",
            "user_info",
            "reason",
            "description",
            "created",
            "url",
        ]

        validators = [
            UniqueTogetherValidator(
                queryset=CommentBlame.objects.all(),
                fields=["comment", "user"],
                message="이미 해당 댓글을 신고했습니다.",
            )
        ]

    def get_content(self, obj):
        return obj.comment.comment

    def get_user_info(self, obj):
        user = User.objects.get(id=obj.user.id)
        return UserInfoSerializer(user).data

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())

    def save(self):
        comment_id = self.validated_data["comment"].id
        user_id = self.validated_data["user"].id
        if comment_id != self.context.get("comment_id"):
            raise ValidationError("신고된 댓글 id가 일치하지 않습니다.")
        if user_id != self.context.get("request").user.id:
            raise ValidationError("신고한 유저의 id와 일치하지 않습니다.")
        return super().save()
