from dj_rest_auth.registration.serializers import (
    RegisterSerializer,
    SocialLoginSerializer,
)
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    nickname = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=["nickname"],
                message="이 닉네임은 다른 사용자가 쓰고 있습니다.",
            )
        ]

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.nickname = self.data.get("nickname")
        user.email = self.data.get("email")
        user.save()
        return user


class CustomLoginSerializer(LoginSerializer):
    username = None


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "email",
            "nickname",
            "random_name",
            "profile_image",
            "is_verify",
        )
        read_only_fields = (
            "pk",
            "email",
            "is_verify",
        )


# TODO Social login 할 때 nickname값도 받아와서 저장하도록 수정
class CustomSocialLoginSerializer(SocialLoginSerializer):
    nickname = serializers.CharField(required=False, allow_blank=True)
    refresh_token = serializers.CharField(required=False, allow_blank=True)
    expires_in = serializers.DateTimeField(required=False)
    code = None
    id_token = None
