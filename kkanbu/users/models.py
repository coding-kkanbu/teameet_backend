from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    name = None
    first_name = None
    last_name = None
    
    
    nickname = models.CharField(_("nickname"), max_length=150, unique=True)
    random_name = models.CharField(
        _("random name"), max_length=150, blank=True, null=True
    )
    profile_image = models.ImageField(_("profile"), blank=True, null=True)
    ip = models.GenericIPAddressField(_("user IP"), blank=True, null=True)
    neis_email = models.EmailField(_("NEIS email address"), blank=True, null=True)
    is_verify = models.BooleanField(_("NEIS email verified"), default=False)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
