from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Category, Comment, Post


class PostSerializer(ModelSerializer):
    user = SerializerMethodField()
    comment_n = SerializerMethodField()
    postlike_n = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "category",
            "title",
            "content",
            "tag",
            "postlike_n",
            "comment_n",
            "user",
        ]
        read_only_fields = ["id", "comment_n", "hit", "user", "created", "modified"]

    def get_user(self, obj):
        return str(obj.writer.nickname)

    def get_comment_n(self, obj):
        return obj.comment_set.count()

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
