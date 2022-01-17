"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="tmoDvWS05crD3EfLU8oZ3Inc5ZcPbe2Vboe7eKnmg3HpXlryS1OkA46F464dzy76",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Your stuff...
# ------------------------------------------------------------------------------
BASE_URL = "http://localhost:8000/"

GOOGLE_CLIENT_ID = env("GOOGLE_CLIENT_ID", default="default_google_client_id")
GOOGLE_CLIENT_SECRET = env(
    "GOOGLE_CLIENT_SECRET", default="default_google_client_secret"
)
KAKAO_CLIENT_ID = env("KAKAO_CLIENT_ID", default="default_kakao_client_id")

GOOGLE_CALLBACK_URI = BASE_URL + "accounts/google/callback/"
KAKAO_CALLBACK_URI = BASE_URL + "accounts/kakao/callback/"
