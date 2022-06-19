from rest_framework.serializers import ModelSerializer, SerializerMethodField

from kkanbu.board.models import Category, Comment, Post, SogaetingOption
from kkanbu.operation.serializers import CommentLikeSerializer, PostLikeSerializer
from kkanbu.users.models import User


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


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "random_name",
        ]


class PostListSerializer(ModelSerializer):
    sogaetingoption = SogaetingOptionSerializer(read_only=True)
    postlike_n = SerializerMethodField()
    comment_n = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "sogaetingoption",
            "title",
            "content",
            "created",
            "hit",
            "postlike_n",
            "comment_n",
        ]

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()

    def get_comment_n(self, obj):
        return obj.comment_set.filter(is_show=True).count()


class PostSerializer(ModelSerializer):
    category_set = SerializerMethodField()
    writer = UserSerializer(read_only=True)
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
            "tag",
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


class PitAPatSerializer(ModelSerializer):
    category_set = SerializerMethodField()
    sogaetingoption = SogaetingOptionSerializer()
    writer = UserSerializer(read_only=True)
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
            "tag",
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
        tags = validated_data.pop("tag")
        post = Post.objects.create(**validated_data)
        post.tag.set(tags)
        sogaeting_data["post"] = post
        SogaetingOption.objects.create(**sogaeting_data)
        return post

    def update(self, instance, validated_data):
        sogaeting_data = validated_data.pop("sogaetingoption")
        tags = validated_data.pop("tag")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.tag.set(tags)
        sogaeting_obj = SogaetingOption.objects.get(post=instance)
        for attr, value in sogaeting_data.items():
            setattr(sogaeting_obj, attr, value)
        sogaeting_obj.save()
        return instance


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    username = SerializerMethodField()
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
            "username",
            "created",
            "commentlike_n",
            "commentlike_set",
        ]

    def get_username(self, obj):
        return str(obj.writer.nickname)

    def get_commentlike_n(self, obj):
        return obj.commentlike_set.count()
