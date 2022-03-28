from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Category, Comment, Post


class PostSerializer(ModelSerializer):
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
            "postlike_n",
            "comment_n",
            "username",
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
    post_set = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "post_set",
        ]


class CommentSerializer(ModelSerializer):
    username = SerializerMethodField()
    commentlike_n = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "comment",
            "secret",
            "username",
            "commentlike_n",
        ]

    def get_username(self, obj):
        return str(obj.writer.nickname)

    def get_commentlike_n(self, obj):
        return obj.commentlike_set.count()
