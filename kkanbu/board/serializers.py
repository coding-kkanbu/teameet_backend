from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Category, Comment, Post


class PostSerializer(ModelSerializer):
    user = SerializerMethodField()
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
            "comment_n",
            "postlike_n",
            "hit",
            "user",
            "created",
            "modified",
        ]

    def get_user(self, obj):
        return str(obj.writer.nickname)

    def get_comment_n(self, obj):
        return obj.comment_set.count()

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()


class BoardListSerializer(ModelSerializer):
    post_set = SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "post_set",
        ]

    def get_post_set(self, obj):
        posts = obj.post_set.order_by("-created")[:5]
        return PostSerializer(posts, many=True).data


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "category",
            "title",
            "content",
            "tag",
        ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
