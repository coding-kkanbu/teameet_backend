from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# for backend test > should be implemented on frontend
@api_view(["GET"])
@permission_classes([AllowAny])
def get_callback(request):
    code = request.GET.get("code")
    return Response({"code": code})


google_oauth2_login = google_views.oauth2_login
kakao_oauth2_login = kakao_views.oauth2_login


class GoogleLogin(SocialLoginView):
    adapter_class = google_views.GoogleOAuth2Adapter
    client_class = OAuth2Client
    # TODO production 단계에서 callback_url 수정
    callback_url = settings.GOOGLE_CALLBACK_URI


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
    # TODO production 단계에서 callback_url 수정
    callback_url = settings.KAKAO_CALLBACK_URI
