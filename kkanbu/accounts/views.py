# Create your views here.
from json.decoder import JSONDecodeError

import environ
import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import status

from kkanbu.users.models import User

env = environ.Env()

BASE_URL = "http://localhost:8000/"


GOOGLE_CLIENT_ID = env("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = env("GOOGLE_CLIENT_SECRET")
KAKAO_CLIENT_ID = env("KAKAO_CLIENT_ID")

GOOGLE_CALLBACK_URI = "http://localhost:8000/accounts/google/callback"
KAKAO_CALLBACK_URI = "http://localhost:8000/accounts/kakao/callback/"


def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}"
        f"&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
    )


def google_callback(request):
    code = request.GET.get("code")
    state = "random string"
    print(code, state)
    access_token = request_access_token(
        f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret="
        f"{GOOGLE_CLIENT_SECRET}&code={code}&grant_type=authorization_code&redirect_uri="
        f"{GOOGLE_CALLBACK_URI}&state={state}"
    )
    print("access token: ", access_token)
    data = request_data(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
    )
    email = data.get("email")
    print("email: ", email)
    json_response = signup_or_sign_in(code, email, access_token, provider="google")
    return json_response


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


def kakao_login(request):
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_uri="
        f"{KAKAO_CALLBACK_URI}&response_type=code"
    )


def kakao_callback(request):
    code = request.GET.get("code")
    print(code)
    access_token = request_access_token(
        "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id="
        f"{KAKAO_CLIENT_ID}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
    )
    data = request_data(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    email = data.get("kakao_account").get("email")
    print("email: ", email)
    json_response = signup_or_sign_in(code, email, access_token, provider="kakao")
    return json_response


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI


def request_access_token(url):
    """
    Access Token Request
    """
    token_req = requests.post(url)
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    return token_req_json.get("access_token")


def request_data(url, headers=None):
    """
    Data Request
    """
    req = requests.get(url, headers=headers)
    req_status = req.status_code
    if req_status != 200:
        return JsonResponse(
            {"err_msg": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
        )
    return req.json()


def signup_or_sign_in(code, email, access_token, provider):
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != provider:
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 Google로 가입된 유저
        data = {"access_token": access_token, "code": code}

        return JsonResponse(data)

    except User.DoesNotExist:
        print("signing up")
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code}

        return JsonResponse(data)
