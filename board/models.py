from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    title = models.CharField(max_length=128)
    category = models.ManyToManyField(Category)
    tag = models.ManyToManyField("Tag", blank=True)
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
            models.UniqueConstraint(
                fields=["title", "writer"],
                name="unique title, writer",
            )
        ]


class SogaetingOption(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    region = models.CharField(max_length=30)
    gender = models.PositiveIntegerField(default=1)
    age = models.PositiveIntegerField(default=24)


class PostLike(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} | {self.user}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "user"],
                name="unique post, user",
            )
        ]


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Comment(TimeStampedModel):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_show = models.BooleanField(default=True)
    secret = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"[{self.id}]{self.comment[:10]} | {self.writer}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["comment", "writer"],
                name="unique comment, writer",
            )
        ]


class CommentLike(TimeStampedModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment} | {self.user}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["comment", "user"],
                name="unique comment, user",
            )
        ]
