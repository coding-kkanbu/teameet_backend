import jwt
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from kkanbu.accounts.serializers import (
    VerifyNeisEmailConfirmSerializer,
    VerifyNeisEmailSerializer,
)
from kkanbu.accounts.utils import send_email

User = get_user_model()


@extend_schema(tags=["accounts"])
def get_redirect_url(adapter, provider_name, callback_url, scope):
    app = SocialApp.objects.get(provider=provider_name)
    params = {
        "client_id": app.client_id,
        "redirect_uri": callback_url,
        "response_type": "code",
    }
    if scope:
        params.update({"scope": "+".join(scope)})
    return "{}?{}".format(adapter.authorize_url, urlencode(params).replace("%2B", "+"))


@extend_schema(tags=["accounts"])
@api_view(["GET"])
@permission_classes([AllowAny])
def get_google_redirect_url(request):
    try:
        scope = settings.SOCIALACCOUNT_PROVIDERS["google"]["SCOPE"]
    except KeyError:
        scope = None

    url = get_redirect_url(
        google_views.GoogleOAuth2Adapter, "google", settings.GOOGLE_CALLBACK_URI, scope
    )
    return Response({"url": url})


@extend_schema(tags=["accounts"])
@api_view(["GET"])
@permission_classes([AllowAny])
def get_kakao_redirect_url(request):
    try:
        scope = settings.SOCIALACCOUNT_PROVIDERS["kakao"]["SCOPE"]
    except KeyError:
        scope = None
    url = get_redirect_url(
        kakao_views.KakaoOAuth2Adapter, "kakao", settings.KAKAO_CALLBACK_URI, scope
    )
    return Response({"url": url})


# for backend test > should be implemented on frontend
@extend_schema(tags=["accounts"])
@api_view(["GET"])
@permission_classes([AllowAny])
def get_callback(request):
    code = request.GET.get("code")
    return Response({"code": code})


@extend_schema(tags=["accounts"])
class GoogleLogin(SocialLoginView):
    adapter_class = google_views.GoogleOAuth2Adapter
    client_class = OAuth2Client
    # TODO production 단계에서 callback_url 수정
    callback_url = settings.GOOGLE_CALLBACK_URI


@extend_schema(tags=["accounts"])
class KakaoLogin(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
    # TODO production 단계에서 callback_url 수정
    callback_url = settings.KAKAO_CALLBACK_URI


class VerifyNeisEmail(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyNeisEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        local = serializer.data["email_local"]
        domain = serializer.data["email_domain"]

        neis_email = local + "@" + domain

        current_site = get_current_site(request).domain
        relative_link = reverse("verify_neis_email_confirm")

        token = AccessToken.for_user(request.user)
        token["neis_email"] = neis_email

        redirect_url = serializer.data.get("redirect_url", "")

        link = (
            "http://"
            + current_site
            + relative_link
            + "?token="
            + str(token)
            + "&redirect_url="
            + redirect_url
        )

        data = {
            "from_email": "Team teameet",
            "to_email": neis_email,
            "email_subject": "티밋 교직원 인증 메일",
            "email_body": f"안녕하세요, 티밋입니다. 교직원 인증을 통해 더 많은 서비스를 이용하시겠습니까?\n아래 링크를 눌러주세요.\n{link} ",
        }
        send_email(data)
        return Response(
            {"message": "Email was successfully sent"}, status=status.HTTP_200_OK
        )


class VerifyNeisEmailConfirm(GenericAPIView):
    serializer_class = VerifyNeisEmailConfirmSerializer

    def get(self, request):
        token = request.query_params.get("token")
        redirect_url = request.query_params.get("redirect_url") or settings.FRONTEND_URL
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            neis_email = payload["neis_email"]
            user.is_verify = True
            user.neis_email = neis_email
            user.save()
            return redirect(redirect_url + "?token_valid=true")

        except jwt.ExpiredSignatureError:
            return redirect(redirect_url + "?token_valid=false")
        except jwt.exceptions.DecodeError:
            return redirect(redirect_url + "?token_valid=false")
