from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from kkanbu.operation.serializers import CommentLikeSerializer, PostLikeSerializer

from .models import Category, Comment, Post


class CategoryForeignKey(PrimaryKeyRelatedField):
    def get_queryset(self):
        return Category.objects.filter(app="Topic")


class PostListSerializer(ModelSerializer):
    category = CategoryForeignKey()
    username = SerializerMethodField()
    comment_n = SerializerMethodField()
    postlike_n = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "category",
            "title",
            "content",
            "tag",
            "username",
            "postlike_n",
            "comment_n",
            "hit",
        ]
        read_only_fields = [
            "hit",
        ]

    def get_username(self, obj):
        return str(obj.writer.nickname)

    def get_comment_n(self, obj):
        return obj.comment_set.filter(is_show=True).count()

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()


class CategorySerializer(ModelSerializer):
    recent_posts = SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "recent_posts",
        ]

    def get_recent_posts(self, obj):
        recent_posts = Post.objects.filter(is_show=True, category=obj).order_by(
            "-created"
        )[:5]
        serializer = PostListSerializer(recent_posts, many=True)
        return serializer.data


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
        read_only_fields = [
            "is_show",
        ]

    def get_username(self, obj):
        return str(obj.writer.nickname)

    def get_commentlike_n(self, obj):
        return obj.commentlike_set.count()


class PostDetailSerializer(ModelSerializer):
    category = CategoryForeignKey()
    username = SerializerMethodField()
    postlike_n = SerializerMethodField()
    postlike_set = PostLikeSerializer(many=True, read_only=True)
    comment_n = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "category",
            "title",
            "content",
            "created",
            "tag",
            "username",
            "hit",
            "ip",
            "postlike_n",
            "postlike_set",
            "comment_n",
        ]
        read_only_fields = [
            "hit",
            "ip",
        ]

    def get_username(self, obj):
        return str(obj.writer.nickname)

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()

    def get_comment_n(self, obj):
        return obj.comment_set.filter(is_show=True).count()
