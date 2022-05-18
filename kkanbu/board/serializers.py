from rest_framework.serializers import ModelSerializer, SerializerMethodField

from kkanbu.operation.serializers import CommentLikeSerializer, PostLikeSerializer

from .models import Category, Comment, Post


class PostListSerializer(ModelSerializer):
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
            "username",
            "postlike_n",
            "comment_n",
            "hit",
            "created",
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


class PostDetailSerializer(ModelSerializer):
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
            "postlike_n",
            "postlike_set",
            "comment_n",
        ]

    def get_username(self, obj):
        return str(obj.writer.nickname)

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()

    def get_comment_n(self, obj):
        return obj.comment_set.filter(is_show=True).count()
