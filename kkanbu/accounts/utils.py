import requests
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from .exceptions import SocialAuthError

User = get_user_model()


def request_access_token(url):
    """
    Access Token Request
    """
    token_req = requests.post(url)
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise SocialAuthError("code for social auth is invalid")
    return token_req_json.get("access_token")


def request_data(url, headers=None):
    """
    Data Request
    """
    req = requests.get(url, headers=headers)
    req_status = req.status_code
    if req_status != 200:
        return SocialAuthError("failed to get email")
    return req.json()


def check_user_exists(email, name, access_token, provider):
    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return SocialAuthError("email exists but not social user")
        if social_user.provider != provider:
            return SocialAuthError("no matching social type")
        # 기존에 가입된 유저
        data = {
            "access_token": access_token,
            "signed_up_state": "AccountExists",
            "nickname": user.nickname,
        }
        return Response(data)

    except User.DoesNotExist:
        # 기존에 가입되어 있지 않은 유저
        data = {
            "access_token": access_token,
            "signed_up_state": "AccountNotExists",
            "nickname": name,
        }
        return Response(data)
