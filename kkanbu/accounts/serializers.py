from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from jsonschema import ValidationError
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


class VerifyNeisEmailConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()


class VerifyNeisEmailSerializer(serializers.Serializer):
    email_local = serializers.CharField(allow_blank=False, allow_null=False)
    email_domain = serializers.ChoiceField(
        choices=[
            "gmail.com",
            "sen.go.kr",
            "pen.go.kr",
            "dge.go.kr",
            "ice.go.kr",
            "gen.go.kr",
            "dje.go.kr",
            "use.go.kr",
            "sje.go.kr",
            "goe.go.kr",
            "gwe.go.kr",
            "cbe.go.kr",
            "cne.go.kr",
            "jbe.go.kr",
            "jne.go.kr",
            "gbe.go.kr",
            "gne.go.kr",
            "jje.go.kr",
        ]
    )

    def validate(self, data):
        user = self.context["request"].user
        if user.is_verify:
            raise ValidationError("Neis email already verified.")
        return data
