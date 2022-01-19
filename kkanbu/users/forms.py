from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    nickname = forms.CharField(label=_("nickname"), widget=forms.TextInput)

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        fields = ["username", "password1", "password2", "nickname"]

        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
            "nickname": {"unique": _("This nickname has already been taken.")},
        }
