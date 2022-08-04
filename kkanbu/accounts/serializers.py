from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

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
    neis_email = serializers.EmailField(
        allow_blank=False,
        allow_null=False,
        validators=[UniqueValidator(queryset=User.objects.filter(is_verify=True))],
    )
    redirect_url = serializers.CharField(max_length=500, required=False)

    def validate_neis_email(self, value):
        domains = [
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
        domain_index = value.find("@") + 1
        domain = value[domain_index:]
        if domain not in domains:
            raise ValidationError("Not valid neis domain.")
        return value

    def validate(self, data):
        user = self.context["request"].user
        if user.is_verify:
            raise ValidationError("User already verified.")
        return data
