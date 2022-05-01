from rest_framework import serializers

from kkanbu.board.models import Category, Post, SogaetingOption
from kkanbu.operation.serializers import PostLikeSerializer


class SogaetingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SogaetingOption
        fields = [
            "post",
            "region",
            "gender",
            "age",
            "connected",
        ]
        read_only_fields = [
            "post",
            "connected",
        ]


class CategoryForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Category.objects.filter(app="PitAPat")


class PitAPatListSerializer(serializers.ModelSerializer):
    sogaetingoption = SogaetingOptionSerializer()
    category = CategoryForeignKey()
    comment_n = serializers.SerializerMethodField()
    postlike_n = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "sogaetingoption",
            "id",
            "category",
            "title",
            "content",
            "tag",
            "postlike_n",
            "comment_n",
            "hit",
            "created",
        ]
        read_only_fields = [
            "hit",
        ]

    def create(self, validated_data):
        return Post.objects.get(id=validated_data["post_id"])

    def get_comment_n(self, obj):
        return obj.comment_set.filter(is_show=True).count()

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()


class PitAPatDetailSerializer(serializers.ModelSerializer):
    sogaetingoption = SogaetingOptionSerializer()
    category = CategoryForeignKey()
    username = serializers.SerializerMethodField()
    postlike_n = serializers.SerializerMethodField()
    postlike_set = PostLikeSerializer(many=True, read_only=True)
    comment_n = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "sogaetingoption",
            "id",
            "category",
            "title",
            "content",
            "created",
            "modified",
            "tag",
            "username",
            "hit",
            "postlike_n",
            "postlike_set",
            "comment_n",
        ]
        read_only_fields = [
            "hit",
        ]

    def update(self, instance, validated_data):
        sogaeting = validated_data.pop("sogaetingoption")
        for key, val in sogaeting.items():
            setattr(instance.sogaetingoption, key, val)
        tags = validated_data.pop("tag")
        instance.tag.set(tags)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_username(self, obj):
        return str(obj.writer.nickname)

    def get_postlike_n(self, obj):
        return obj.postlike_set.count()

    def get_comment_n(self, obj):
        return obj.comment_set.filter(is_show=True).count()
