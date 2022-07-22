from dj_rest_auth.registration.serializers import SocialLoginSerializer
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
            "username",
            "random_name",
            "profile_image",
            "is_verify",
        )
        read_only_fields = (
            "pk",
            "email",
            "is_verify",
        )


# TODO Social login 할 때 username값도 받아와서 저장하도록 수정
class CustomSocialLoginSerializer(SocialLoginSerializer):
    # nickname = serializers.CharField(required=False, allow_blank=True)
    refresh_token = serializers.CharField(required=False, allow_blank=True)
    expires_in = serializers.DateTimeField(required=False)
    code = None
    id_token = None
