from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    DateTimeField,
    ModelSerializer,
    SerializerMethodField,
    SlugRelatedField,
)
from taggit.serializers import TaggitSerializer, TagListSerializerField

from kkanbu.board.helpers.utils import AppTypeValidator, TextLengthValidator
from kkanbu.board.models import Category, Comment, Post, SogaetingOption
from kkanbu.operation.serializers import CommentLikeSerializer, PostLikeSerializer
from kkanbu.users.api.serializers import UserInfoSerializer


class SogaetingOptionSerializer(ModelSerializer):
    class Meta:
        model = SogaetingOption
        fields = [
            "region",
            "gender",
            "age",
            "connected",
        ]
        read_only_fields = ["connected"]
        extra_kwargs = {
            "region": {"error_messages": {"invalid_choice": "올바른 지역을 입력해주세요."}},
            "gender": {"error_messages": {"invalid_choice": "올바른 성별을 입력해주세요."}},
        }

    def validate_age(self, value):
        if value < 20:
            raise ValidationError("올바른 나이를 입력해주세요.")
        return value


class PostListSerializer(ModelSerializer):
    sogaetingoption = SogaetingOptionSerializer(read_only=True)
    tags = TagListSerializerField()
    postlike_n = SerializerMethodField()
    comment_n = SerializerMethodField()
    timesince = DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "sogaetingoption",
            "title",
            "content",
            "tags",
            "created",
            "timesince",
            "hit",
            "postlike_n",
            "comment_n",
        ]

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()

    def get_comment_n(self, obj):
        return obj.comment_set.filter(is_show=True).count()


class PostSerializer(TaggitSerializer, ModelSerializer):
    category_set = SerializerMethodField()
    category = SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        validators=[AppTypeValidator(app_type="Topic")],
    )
    title = CharField(max_length=128, validators=[TextLengthValidator(min_length=4)])
    content = CharField(
        style={"base_template": "textarea.html"},
        validators=[TextLengthValidator(min_length=4)],
    )
    timesince = DateTimeField(read_only=True)
    tags = TagListSerializerField()
    writer = UserInfoSerializer(read_only=True)
    postlike_n = SerializerMethodField()
    postlike_set = PostLikeSerializer(many=True, read_only=True)
    comment_n = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "category_set",
            "category",
            "title",
            "content",
            "created",
            "timesince",
            "tags",
            "writer",
            "hit",
            "postlike_n",
            "postlike_set",
            "comment_n",
        ]
        read_only_fields = ["hit"]

    def get_category_set(self, obj):
        cat = Category.objects.get(post=obj)
        serializer = CategorySerializer(cat)
        return serializer.data

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()

    def get_comment_n(self, obj):
        return obj.comment_set.filter(is_show=True).count()


class PitAPatSerializer(TaggitSerializer, ModelSerializer):
    category_set = SerializerMethodField()
    sogaetingoption = SogaetingOptionSerializer()
    category = SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        validators=[AppTypeValidator(app_type="PitAPat")],
    )
    title = CharField(max_length=128, validators=[TextLengthValidator(min_length=4)])
    content = CharField(
        style={"base_template": "textarea.html"},
        validators=[TextLengthValidator(min_length=4)],
    )
    timesince = DateTimeField(read_only=True)
    tags = TagListSerializerField()
    writer = UserInfoSerializer(read_only=True)
    postlike_n = SerializerMethodField()
    postlike_set = PostLikeSerializer(many=True, read_only=True)
    comment_n = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "category_set",
            "sogaetingoption",
            "category",
            "title",
            "content",
            "created",
            "timesince",
            "tags",
            "writer",
            "hit",
            "postlike_n",
            "postlike_set",
            "comment_n",
        ]
        read_only_fields = ["hit"]

    def get_category_set(self, obj):
        cat = Category.objects.get(post=obj)
        serializer = CategorySerializer(cat)
        return serializer.data

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()

    def get_comment_n(self, obj):
        return obj.comment_set.filter(is_show=True).count()

    def create(self, validated_data):
        sogaeting_data = validated_data.pop("sogaetingoption")
        to_be_tagged, validated_data = self._pop_tags(validated_data)
        post = Post.objects.create(**validated_data)
        tagged_post = self._save_tags(post, to_be_tagged)
        sogaeting_data["post"] = tagged_post
        SogaetingOption.objects.create(**sogaeting_data)
        return tagged_post

    def update(self, instance, validated_data):
        sogaeting_data = validated_data.pop("sogaetingoption")
        to_be_tagged, validated_data = self._pop_tags(validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        tagged_instance = self._save_tags(instance, to_be_tagged)
        sogaeting_obj = SogaetingOption.objects.get(post=tagged_instance)
        for attr, value in sogaeting_data.items():
            setattr(sogaeting_obj, attr, value)
        sogaeting_obj.save()
        return tagged_instance


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    writer = UserInfoSerializer(read_only=True)
    timesince = DateTimeField(read_only=True)
    commentlike_n = SerializerMethodField()
    commentlike_set = CommentLikeSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "parent_comment",
            "comment",
            "secret",
            "is_show",
            "writer",
            "created",
            "timesince",
            "commentlike_n",
            "commentlike_set",
            "child_comments",
        ]
        read_only_fields = ["post", "parent_comment", "is_show"]

    def get_fields(self):
        fields = super(CommentSerializer, self).get_fields()
        fields["child_comments"] = CommentSerializer(many=True, read_only=True)
        return fields

    def get_commentlike_n(self, obj):
        return obj.commentlike_set.count()

    def to_representation(self, instance: Comment):
        ret = super().to_representation(instance)
        # is_show False인 instance 필터링
        if not instance.is_show:
            return None
        user = self.context["request"].user
        post = self.context.get("post", None)
        if instance.secret:
            if (
                user == instance.writer
                or user == getattr(instance.parent_comment, "writer", None)
                or user == getattr(post, "writer", None)
            ):
                pass
            else:
                ret["comment"] = "[글 작성자와 댓글 작성자만 볼 수 있는 댓글입니다]"
        return ret


class CommentListSerializer(ModelSerializer):
    writer = UserInfoSerializer(read_only=True)
    comment = CharField(
        style={"base_template": "textarea.html"},
        validators=[TextLengthValidator(min_length=4, message="댓글은 4글자 이상 입력해 주세요.")],
    )
    timesince = DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "parent_comment",
            "comment",
            "writer",
            "secret",
            "is_show",
            "created",
            "timesince",
        ]
        read_only_fields = ["is_show"]

    def validate(self, data):
        """
        Check that comment post pk is the same as parent comment pk
        """
        if data["parent_comment"] and data["parent_comment"].post.id != data["post"].id:
            raise ValidationError(
                "post pk should be the same as parent comment post pk"
            )
        return data
