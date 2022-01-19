from dj_rest_auth.registration.views import RegisterView  # VerifyEmailView
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    UserDetailsView,
)
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
    path("register/", RegisterView.as_view(), name="account_signup"),
    path("login/", LoginView.as_view(), name="account_login"),
    path("logout/", LogoutView.as_view(), name="account_logout"),
    path("user/", UserDetailsView.as_view()),
    # 로그인된 유저가 password 바꿀때
    path("password-change/", PasswordChangeView.as_view()),
    # password 분실로 로그인이 안될때
    path("password-reset/", PasswordResetView.as_view()),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("google/login", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
    path("google/login/finish/", GoogleLogin.as_view(), name="google_login_todjango"),
    path("kakao/login", kakao_login, name="kakao_login"),
    path("kakao/callback/", kakao_callback, name="kakao_callback"),
    path("kakao/login/finish/", KakaoLogin.as_view(), name="kakao_login_todjango"),
]
