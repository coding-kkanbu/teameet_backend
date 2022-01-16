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
