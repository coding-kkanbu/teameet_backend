import environ
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .serializers import CustomSocialLoginSerializer
from .utils import check_user_exists, request_access_token, request_data

env = environ.Env()

GOOGLE_CLIENT_ID = SocialApp.objects.get(provider="google").client_id
GOOGLE_CLIENT_SECRET = SocialApp.objects.get(provider="google").secret
KAKAO_CLIENT_ID = SocialApp.objects.get(provider="kakao").client_id

GOOGLE_CALLBACK_URI = settings.GOOGLE_CALLBACK_URI
KAKAO_CALLBACK_URI = settings.KAKAO_CALLBACK_URI

User = get_user_model()


# for backend test > should be implemented on frontend
def get_callback(request):
    code = request.GET.get("code")
    return JsonResponse({"code": code})


@api_view(("GET",))
@permission_classes([AllowAny])
def google_account_exists(request):
    code = request.GET.get("code")
    access_token = request_access_token(
        f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}"
        f"&client_secret={GOOGLE_CLIENT_SECRET}&code={code}&grant_type=authorization_code"
        f"&redirect_uri={GOOGLE_CALLBACK_URI}"
    )
    data = request_data(
        "https://www.googleapis.com/oauth2/v1/userinfo?alt=json",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    email = data.get("email")
    name = data.get("name")
    response = check_user_exists(email, name, access_token, provider="google")
    return response


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client

    serializer_class = CustomSocialLoginSerializer


@api_view(("GET",))
@permission_classes([AllowAny])
def kakao_account_exists(request):
    code = request.GET.get("code")
    access_token = request_access_token(
        "https://kauth.kakao.com/oauth/token?grant_type=authorization_code"
        f"&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
    )
    data = request_data(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    email = data.get("kakao_account").get("email")
    name = data.get("properties").get("nickname")
    response = check_user_exists(email, name, access_token, provider="kakao")
    return response


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI

    serializer_class = CustomSocialLoginSerializer
