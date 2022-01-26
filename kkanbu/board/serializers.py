from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Category, Comment, Post


class PostSerializer(ModelSerializer):
    user = SerializerMethodField()
    comment_n = SerializerMethodField()
    postlike_n = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "title",
            "comment_n",
            "postlike_n",
            "hit",
            "user",
            "created",
        ]

    def get_user(self, obj):
        return str(obj.writer.nickname)

    def get_comment_n(self, obj):
        return obj.comment_set.count()

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()


class MainListSerializer(ModelSerializer):
    post_set = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "name",
            "post_set",
        ]


# class PostSerializer(ModelSerializer):
#     class Meta:
#         model = Post
#         fields = "__all__"


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
