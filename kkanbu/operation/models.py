from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

from kkanbu.board.models import Comment, Post

User = settings.AUTH_USER_MODEL


class PostBlame(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} blamed by {self.user}"


class CommentBlame(TimeStampedModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment} blamed by {self.user}"
