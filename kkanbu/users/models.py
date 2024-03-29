import os

from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from kkanbu.users.utils import generate_random_name


def profile_image_file_path(instance, filename):
    """Generate file path for new profile image."""
    return os.path.join("uploads", "profile", filename)


class User(AbstractUser):
    email_validator = EmailValidator()

    email = models.EmailField(
        _("email address"),
        unique=True,
        validators=[email_validator],
        error_messages={
            "unique": _("An address with that email already exists."),
        },
    )

    first_name = None
    last_name = None
    random_name = models.CharField(
        _("random name"), max_length=150, blank=True, null=True
    )
    introduce = models.TextField(_("introduce"), blank=True, null=True)
    profile_image = models.ImageField(
        _("profile"), blank=True, null=True, upload_to=profile_image_file_path
    )
    ip = models.GenericIPAddressField(_("user IP"), blank=True, null=True)
    neis_email = models.EmailField(_("NEIS email address"), blank=True, null=True)
    is_verify = models.BooleanField(_("NEIS email verified"), default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        if not self.random_name:
            self.random_name = generate_random_name()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["neis_email"],
                condition=Q(is_verify=True),
                name="unique_neis_email",
            )
        ]
