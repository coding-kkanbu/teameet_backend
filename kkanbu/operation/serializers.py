from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)

from kkanbu.users.api.serializers import UserInfoSerializer

from .models import CommentBlame, CommentLike, PostBlame, PostLike

User = get_user_model()


class PostLikeSerializer(ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    url = SerializerMethodField()

    class Meta:
        model = PostLike
        fields = ["id", "post", "user", "created", "url"]
        read_only_fields = ["post"]

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        post_id = validated_data["post"].id
        user_id = validated_data["user"].id
        post_like = PostLike.objects.filter(Q(post__id=post_id) & Q(user__id=user_id))
        if post_like:
            post_like.delete()
            return None
        return super().save(**validated_data)


class CommentLikeSerializer(ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    url = SerializerMethodField()

    class Meta:
        model = CommentLike
        fields = ["id", "comment", "user", "created", "url"]
        read_only_fields = ["comment"]

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        comment_id = validated_data["comment"].id
        user_id = validated_data["user"].id
        comment_like = CommentLike.objects.filter(
            Q(comment__id=comment_id) & Q(user__id=user_id)
        )
        if comment_like:
            comment_like.delete()
            return None
        return super().save(**validated_data)


class PostBlameSerializer(ModelSerializer):
    post = StringRelatedField()
    user = UserInfoSerializer(read_only=True)
    url = SerializerMethodField()

    class Meta:
        model = PostBlame
        fields = [
            "id",
            "post",
            "user",
            "reason",
            "description",
            "created",
            "url",
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        post_id = validated_data["post"].id
        user_id = validated_data["user"].id
        if PostBlame.objects.filter(Q(post__id=post_id) & Q(user__id=user_id)).exists():
            raise ValidationError("이미 해당 게시물을 신고했습니다.")
        return super().save(**validated_data)


class CommentBlameSerializer(ModelSerializer):
    comment = StringRelatedField()
    user = UserInfoSerializer(read_only=True)
    url = SerializerMethodField()

    class Meta:
        model = CommentBlame
        fields = [
            "id",
            "comment",
            "user",
            "reason",
            "description",
            "created",
            "url",
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        comment_id = validated_data["comment"].id
        user_id = validated_data["user"].id
        # TODO UniqueTogtherValidtor 커스터마이징 해보기
        if CommentBlame.objects.filter(
            Q(comment__id=comment_id) & Q(user__id=user_id)
        ).exists():
            raise ValidationError("이미 해당 댓글을 신고했습니다.")
        return super().save(**validated_data)
