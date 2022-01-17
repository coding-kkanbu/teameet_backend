from django.urls import path

from .views import (
    GoogleLogin,
    KakaoLogin,
    google_callback,
    google_login,
    kakao_callback,
    kakao_login,
)

urlpatterns = [
    path("google/login", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
    path("google/login/finish/", GoogleLogin.as_view(), name="google_login_todjango"),
    path("kakao/login", kakao_login, name="kakao_login"),
    path("kakao/callback/", kakao_callback, name="kakao_callback"),
    path("kakao/login/finish/", KakaoLogin.as_view(), name="kakao_login_todjango"),
]
