from rest_framework.exceptions import APIException


class SocialAuthError(APIException):
    status_code = 400
    default_detail = "Authentication with social account unavailable."
    default_code = "social_auth_error"
