from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.utils.http import urlencode
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# for backend test > should be implemented on frontend
@extend_schema(tags=["accounts"])
@api_view(["GET"])
@permission_classes([AllowAny])
def get_callback(request):
    code = request.GET.get("code")
    return Response({"code": code})


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
