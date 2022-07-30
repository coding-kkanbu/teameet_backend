from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    username = None


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "email",
            "random_name",
            "profile_image",
            "is_verify",
        )
        read_only_fields = (
            "pk",
            "email",
            "is_verify",
        )
