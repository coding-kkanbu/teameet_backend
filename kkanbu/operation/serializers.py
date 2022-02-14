from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from .models import CommentBlame, PostBlame


class PostBlameSerializer(ModelSerializer):
    class Meta:
        model = PostBlame
        fields = ["post", "user"]

        validators = [
            UniqueTogetherValidator(
                queryset=PostBlame.objects.all(), fields=["post", "user"]
            )
        ]


class CommentBlameSerializer(ModelSerializer):
    class Meta:
        model = CommentBlame
        fields = ["comment", "user"]

        validators = [
            UniqueTogetherValidator(
                queryset=CommentBlame.objects.all(), fields=["comment", "user"]
            )
        ]
