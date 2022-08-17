from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings


class CustomJWTCookieAuthentication(JWTCookieAuthentication):
    """Custom Authentication Class for detail error message handling"""

    def authenticate(self, request):
        cookie_name = getattr(settings, "JWT_AUTH_COOKIE", None)
        header = self.get_header(request)
        if header is None:
            if cookie_name:
                raw_token = request.COOKIES.get(cookie_name)
                if raw_token is not None:
                    self.enforce_csrf(request)
            else:
                return None
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )

        raise TokenUnavailable(
            {
                "detail": _("유효하지 않거나 만료된 토큰입니다"),
                "messages": messages,
            }
        )


class TokenUnavailable(InvalidToken):
    status_code = status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED
