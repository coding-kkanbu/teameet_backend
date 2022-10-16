import os

from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class RegionType(models.TextChoices):
    SEOUL = "서울"
    BUSAN = "부산"
    DAEGU = "대구"
    INCHEON = "인천"
    GWANGJU = "광주"
    DAEJEON = "대전"
    ULSAN = "울산"
    SEJONG = "세종"
    GYEONGGI = "경기"
    GANGWON = "강원"
    CHUNGBUK = "충북"
    CHUNGNAM = "충남"
    JEONBUK = "전북"
    JEONNAM = "전남"
    GYEONGBUK = "경북"
    GYEONGNAM = "경남"
    JEJU = "제주"


class GenderType(models.TextChoices):
    MALE = "남자"
    FEMALE = "여자"


class AgeType(models.TextChoices):
    TWENTY = "20대"
    THIRTY = "30대"
    FOURTY = "40대"
    FIFTY = "50대"
    SIXTY = "60대"


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
    neis_email = models.EmailField(_("NEIS email address"), blank=True, null=True)
    is_verify = models.BooleanField(_("NEIS email verified"), default=False)

    region = models.CharField(
        max_length=30, choices=RegionType.choices, default=AgeType.TWENTY
    )
    age = models.CharField(
        max_length=30, choices=AgeType.choices, default=AgeType.TWENTY
    )
    gender = models.CharField(
        max_length=30, choices=GenderType.choices, default=AgeType.TWENTY
    )

    introduce = models.TextField(_("introduce"), blank=True, null=True)
    profile_image = models.ImageField(
        _("profile"), blank=True, null=True, upload_to=profile_image_file_path
    )

    ip = models.GenericIPAddressField(_("user IP"), blank=True, null=True)
    first_name = None
    last_name = None

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["neis_email"],
                condition=Q(is_verify=True),
                name="unique_neis_email",
            )
        ]
