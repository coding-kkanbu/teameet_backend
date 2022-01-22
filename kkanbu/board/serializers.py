from rest_framework import serializers

from .models import Comment, Post


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "category",
            "title",
            "writer",
            "hit",
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "category",
            "title",
            "content",
            "tag",
            "writer",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
