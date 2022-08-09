from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlencode, urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from kkanbu.accounts.serializers import VerifyNeisEmailSerializer
from kkanbu.accounts.tokens import neis_verify_token

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
    serializer_class = VerifyNeisEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        neis_email = serializer.data["neis_email"]

        user = request.user
        user.neis_email = neis_email
        user.save()
        # TODO get protocol / password
        current_site = get_current_site(request).domain

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = neis_verify_token.make_token(user)
        relative_link = reverse("verify_neis_email_confirm", args=[uid, token])

        url = "http://" + current_site + relative_link

        message = render_to_string(
            "account/email/template_neis_verify.html",
            {"random_name": user.random_name, "url": url},
        )

        data = {
            "from_email": "Team teameet",
            "recipient_list": [neis_email],
            "subject": "티밋 교직원 인증 메일",
            "message": message,
            "html_message": message,
        }
        send_mail(**data)
        return Response(
            {"message": "Email was successfully sent"}, status=status.HTTP_200_OK
        )


@api_view(["GET"])
def verify_neis_email_confirm(request, uidb64, token):
    print("-" * 100)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print(neis_verify_token.check_token(user, token))

    if user is not None and neis_verify_token.check_token(user, token):
        user.is_verify = True
        user.save()
        return Response(
            {"message": "Neis Email was successfully verified"},
            status=status.HTTP_200_OK,
        )
    elif user is None:
        return Response(
            {"message": "Not valid user"}, status=status.HTTP_400_BAD_REQUEST
        )
    else:
        return Response(
            {"message": "Not valid token"}, status=status.HTTP_400_BAD_REQUEST
        )
