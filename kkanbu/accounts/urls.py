from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView  # VerifyEmailView
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.urls import path
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (
    GoogleLogin,
    KakaoLogin,
    VerifyNeisEmail,
    get_callback,
    get_google_redirect_url,
    get_kakao_redirect_url,
    verify_neis_email_confirm,
)

RegisterView.authentication_classes = [BasicAuthentication]
LoginView.authentication_classes = [BasicAuthentication]
PasswordResetView.authentication_classes = [BasicAuthentication]
PasswordResetConfirmView.authentication_classes = [BasicAuthentication]
TokenVerifyView.authentication_classes = [BasicAuthentication]
RefreshView = get_refresh_view()
RefreshView.authentication_classes = [BasicAuthentication]

urlpatterns = [
    path("register/", RegisterView.as_view(), name="account_signup"),
    path("login/", LoginView.as_view(), name="account_login"),
    path("logout/", LogoutView.as_view(), name="account_logout"),
    # 로그인된 유저가 password 바꿀때
    path("password-change/", PasswordChangeView.as_view(), name="password_change"),
    # TODO Edit SMTP settings EmailBackend when Deployment
    # password 분실로 로그인이 안될때
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # TODO Implemt SocialAccounts Connection 소셜계정 연결 기능 추가
    path("google/login/", get_google_redirect_url, name="google_login"),
    # for backend test > should be implemented on frontend
    path("google/login/callback/", get_callback, name="google_callback"),
    path("google/login/finish/", GoogleLogin.as_view(), name="google_login_todjango"),
    path("kakao/login/", get_kakao_redirect_url, name="kakao_login"),
    # for backend test > should be implemented on frontend
    path("kakao/login/callback/", get_callback, name="kakao_callback"),
    path("kakao/login/finish/", KakaoLogin.as_view(), name="kakao_login_todjango"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", RefreshView.as_view(), name="token_refresh"),
    path("verify-neis-email/", VerifyNeisEmail.as_view(), name="verify_neis_email"),
    path(
        "verify-neis-email/confirm/<uidb64>/<token>/",
        verify_neis_email_confirm,
        name="verify_neis_email_confirm",
    ),
]
