from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from taggit.managers import TaggableManager

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    class AppType(models.TextChoices):
        TOPIC = "Topic", _("토픽")
        PITAPAT = "PitAPat", _("두근두근")

    app = models.CharField(
        max_length=30, choices=AppType.choices, default=AppType.TOPIC
    )
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=50, allow_unicode=True, unique=True)

    def __str__(self):
        return f"{self.app} | {self.name}"


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


class SogaetingOption(models.Model):
    class RegionType(models.TextChoices):
        SEOUL = "Seoul", _("서울")
        BUSAN = "Busan", _("부산")
        DAEGU = "Daegu", _("대구")
        INCHEON = "Incheon", _("인천")
        GWANGJU = "Gwangju", _("광주")
        DAEJEON = "Daejeon", _("대전")
        ULSAN = "Ulsan", _("울산")
        SEJONG = "Sejong", _("세종")

        GYEONGGI = "Gyeonggi", _("경기")
        GANGWON = "Gangwon", _("강원")
        CHUNGBUK = "Chungbuk", _("충북")
        CHUNGNAM = "Chungnam", _("충남")
        JEONBUK = "jeonbuk", _("전북")
        JEONNAM = "Jeonnam", _("전남")
        GYEONGBUK = "Gyeongbuk", _("경북")
        GYEONGNAM = "Gyeongnam", _("경남")
        JEJU = "Jeju", _("제주")

    class GenderType(models.IntegerChoices):
        MALE = 1, _("남자")
        FEMALE = 2, _("여자")

    post = models.OneToOneField(
        Post, on_delete=models.CASCADE, primary_key=True, related_name="sogaetingoption"
    )
    region = models.CharField(max_length=30, choices=RegionType.choices)
    gender = models.PositiveIntegerField(choices=GenderType.choices)
    age = models.PositiveIntegerField()
    connected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post}  ||  {self.region} - {self.gender} - {self.age}"


class Comment(TimeStampedModel):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="parent_comment_set",
        null=True,
        blank=True,
    )
    is_show = models.BooleanField(default=True)
    secret = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"[{self.id}]{self.comment[:10]} | {self.writer}"
