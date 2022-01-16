from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

User = settings.AUTH_USER_MODEL


class PostBlame(TimeStampedModel):
    post = models.ForeignKey("board.Post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CommentBlame(TimeStampedModel):
    comment = models.ForeignKey("board.Comment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
