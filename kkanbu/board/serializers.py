from kkanbu.operation.serializers import CommentLikeSerializer, PostLikeSerializer
from rest_framework.serializers import ModelSerializer, SerializerMethodField

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
    child_comment = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "parent_comment",
            "comment",
            "secret",
            "username",
            "created",
            "commentlike_n",
            "commentlike_set",
            "child_comment",
        ]

    def get_username(self, obj):
        return str(obj.writer.nickname)

    def get_commentlike_n(self, obj):
        return obj.commentlike_set.count()

    def get_child_comment(self, obj):
        if obj.parent_comment_set:
            child_comments = obj.parent_comment_set.order_by("created")
            for comment in child_comments:
                if comment.secret:
                    if request.user != comment.writer or request.user != post.writer:
                        comment.comment = "[글 작성자와 댓글 작성자만 볼 수 있는 댓글입니다]"
            serializer = CommentSerializer(child_comments, many=True)
            return serializer.data


class PostDetailSerializer(ModelSerializer):
    username = SerializerMethodField()
    postlike_n = SerializerMethodField()
    postlike_set = PostLikeSerializer(many=True, read_only=True)
    comment_n = SerializerMethodField()
    comment_set = SerializerMethodField()

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
            "comment_set",
        ]

    def get_username(self, obj):
        return str(obj.writer.nickname)

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()

    def get_comment_n(self, obj):
        return obj.comment_set.filter(is_show=True).count()

    def get_comment_set(self, obj):
        comment_set = obj.comment_set.filter(parent_comment=None).order_by("created")
        serializer = CommentSerializer(comment_set, many=True)
        return serializer.data
