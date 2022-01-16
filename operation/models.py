from django.db import models
from django_extensions.db.models import TimeStampedModel


class PostBlame(TimeStampedModel):
    post = models.ForeignKey("board.Post", on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "user"],
                name="unique post, user",
            )
        ]


class CommentBlame(TimeStampedModel):
    comment = models.ForeignKey("board.Comment", on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["comment", "user"],
                name="unique comment, user",
            )
        ]
