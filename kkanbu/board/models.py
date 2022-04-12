from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField("Tag", blank=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_show = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    hit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"[{self.id}]{self.title} | {self.writer}"


class SogaetingOption(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    region = models.CharField(max_length=30)
    gender = models.PositiveIntegerField(default=1)
    age = models.PositiveIntegerField(default=24)


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Comment(TimeStampedModel):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.SET_NULL, related_name="parent_comment_set", null=True
    )
    is_show = models.BooleanField(default=True)
    secret = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"[{self.id}]{self.comment[:10]} | {self.writer}"
