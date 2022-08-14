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
            "profile_image",
            "neis_email",
            "is_verify",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }

    def get_post_n(self, obj):
        return obj.post_set.count()


class UserProfileSerializer(serializers.ModelSerializer):
    """한가지 타입의 데이터(사진 파일) upload를 위한 별도 serializer 추가"""

    class Meta:
        model = User
        fields = ["id", "profile_image"]
        extra_kwargs = {"profile_image": {"required": True}}


class UserInfoSerializer(serializers.ModelSerializer):
    """User에 대한 간단한 정보 조회용으로 nested serializer를 위한 객체 추가"""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "random_name",
        ]
