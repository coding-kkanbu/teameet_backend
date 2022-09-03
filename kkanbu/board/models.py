from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.functions import Length
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from taggit.managers import TaggableManager

from kkanbu.notification.models import Notification

models.CharField.register_lookup(Length)
models.TextField.register_lookup(Length)

User = settings.AUTH_USER_MODEL


class AppType(models.TextChoices):
    TOPIC = "Topic", _("토픽")
    PITAPAT = "PitAPat", _("두근두근")


class Category(models.Model):
    app = models.CharField(
        max_length=30, choices=AppType.choices, default=AppType.TOPIC
    )
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=50, allow_unicode=True, unique=True)

    def __str__(self):
        return f"[{self.id}]{AppType(self.app).label} | {self.name} | {self.slug}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(app__in=AppType.values),
                name="%(app_label)s_%(class)s_app_type_valid",
            )
        ]


class Post(TimeStampedModel):
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = TaggableManager()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_show = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    hit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"[{self.id}]{self.title} | {self.writer}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(title__length__gte=4),
                name="%(app_label)s_%(class)s_title_length_gte_4",
            ),
            models.CheckConstraint(
                check=models.Q(content__length__gte=4),
                name="%(app_label)s_%(class)s_content_length_gte_4",
            ),
        ]


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


class GenderType(models.IntegerChoices):
    MALE = 1, _("남자")
    FEMALE = 2, _("여자")


class SogaetingOption(models.Model):
    post = models.OneToOneField(
        Post, on_delete=models.CASCADE, primary_key=True, related_name="sogaetingoption"
    )
    region = models.CharField(max_length=30, choices=RegionType.choices)
    gender = models.PositiveIntegerField(choices=GenderType.choices)
    age = models.PositiveIntegerField()
    connected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post} || {self.region} - {GenderType(self.gender).label} - {self.age}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(region__in=RegionType.values),
                name="%(app_label)s_%(class)s_region_type_valid",
            ),
            models.CheckConstraint(
                check=models.Q(gender__in=GenderType.values),
                name="%(app_label)s_%(class)s_gender_type_valid",
            ),
            models.CheckConstraint(
                check=models.Q(age__gte=20),
                name="%(app_label)s_%(class)s_age_gte_20",
            ),
        ]


class Comment(TimeStampedModel):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="child_comments",
        null=True,
        blank=True,
    )
    is_show = models.BooleanField(default=True)
    secret = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    notifications = GenericRelation(Notification)

    class Meta:
        ordering = ("created",)
        constraints = [
            models.CheckConstraint(
                check=models.Q(comment__length__gte=4),
                name="%(app_label)s_%(class)s_comment_length_gte_4",
            ),
        ]

    def __str__(self):
        return f"[{self.id}]{self.comment[:10]} | {self.writer}"
