from allauth.socialaccount.providers.google.views import (
    oauth2_login as google_oauth2_login,
)
from allauth.socialaccount.providers.kakao.views import (
    oauth2_login as kakao_oauth2_login,
)
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
    get_callback,
    google_account_exists,
    kakao_account_exists,
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
    path("google/login/url", google_oauth2_login, name="google_login"),
    # for backend test > should be implemented on frontend
    path("google/login/callback/", get_callback, name="google_callback"),
    path("google/account-exists", google_account_exists, name="google_account_exists"),
    path("google/login/finish/", GoogleLogin.as_view(), name="google_login_todjango"),
    path("kakao/login/url", kakao_oauth2_login, name="kakao_login"),
    # for backend test > should be implemented on frontend
    path("kakao/login/callback/", get_callback, name="kakao_callback"),
    path("kakao/account-exists", kakao_account_exists, name="kakao_account_exists"),
    path("kakao/login/finish/", KakaoLogin.as_view(), name="kakao_login_todjango"),
]
