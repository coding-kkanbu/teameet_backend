from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    post_n = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "date_joined",
            "random_name",
            "profile_image",
            "introduce",
            "neis_email",
            "is_verify",
            "post_n",
            "url",
        ]

        read_only_fields = [
            "email",
            "date_joined",
            "random_name",
            "neis_email",
            "is_verify",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }

    def get_post_n(self, obj):
        return obj.post_set.count()
