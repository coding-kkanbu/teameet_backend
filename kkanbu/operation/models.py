from django.conf import settings
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django_extensions.db.models import TimeStampedModel

from kkanbu.board.models import Comment, Post

User = settings.AUTH_USER_MODEL


class PostLike(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} liked by {self.user}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["post", "user"],
                name="unique_postlike",
            )
        ]


class CommentLike(TimeStampedModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment} liked by {self.user}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["comment", "user"],
                name="unique_commentlike",
            )
        ]


class PostBlame(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} blamed by {self.user}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=["post", "user"], name="unique_postblame"),
        ]


class CommentBlame(TimeStampedModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment} blamed by {self.user}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=["comment", "user"], name="unique_commentblame"),
        ]
