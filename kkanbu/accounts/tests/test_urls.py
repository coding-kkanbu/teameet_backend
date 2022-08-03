import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_register():
    assert reverse("account_signup") == "/api/v1/accounts/register/"
    assert resolve("/api/v1/accounts/register/").view_name == "account_signup"


def test_login():
    assert reverse("account_login") == "/api/v1/accounts/login/"
    assert resolve("/api/v1/accounts/login/").view_name == "account_login"


def test_logout():
    assert reverse("account_logout") == "/api/v1/accounts/logout/"
    assert resolve("/api/v1/accounts/logout/").view_name == "account_logout"


def test_password_change():
    assert reverse("password_change") == "/api/v1/accounts/password-change/"
    assert resolve("/api/v1/accounts/password-change/").view_name == "password_change"


def test_password_reset():
    assert reverse("password_reset") == "/api/v1/accounts/password-reset/"
    assert resolve("/api/v1/accounts/password-reset/").view_name == "password_reset"


def test_password_reset_confirm():
    uidb64 = "j"
    token = "b8wwzg-db022197f240e88dde8bfc3b3ade3756"
    assert (
        reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
        == f"/api/v1/accounts/password-reset/confirm/{uidb64}/{token}/"
    )
    assert (
        resolve(f"/api/v1/accounts/password-reset/confirm/{uidb64}/{token}/").view_name
        == "password_reset_confirm"
    )


def test_verify_neis_email():
    assert reverse("verify_neis_email") == "/api/v1/accounts/verify-neis-email/"
    assert (
        resolve("/api/v1/accounts/verify-neis-email/").view_name == "verify_neis_email"
    )


def test_verify_neis_email_confirm():
    token = "b8wwzg-db022197f240e88dde8bfc3b3ade3756"
    assert (
        reverse("verify_neis_email_confirm", kwargs={"token": token})
        == f"/api/v1/accounts/verify-neis-email/confirm?token={token}/"
    )
    assert (
        resolve(f"/api/v1/accounts/verify-neis-email/confirm?token={token}/").view_name
        == "verify_neis_email_confirm"
    )
