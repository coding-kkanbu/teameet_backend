from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

User = settings.AUTH_USER_MODEL


class Notification(TimeStampedModel):
    COMMENT = "comment"
    POSTLIKE = "postlike"
    COMMENTLIKE = "commentlike"
    POSTBLAME = "postblame"
    COMMENTBLAME = "commentblame"

    CHOICES = (
        (COMMENT, "Comment"),
        (POSTLIKE, "PostLike"),
        (COMMENTLIKE, "CommentLike"),
        (POSTBLAME, "PostBlame"),
        (COMMENTBLAME, "CommentBlame"),
    )

    user_to = models.ForeignKey(
        User, related_name="notification_to", on_delete=models.CASCADE
    )
    user_by = models.ForeignKey(
        User, related_name="notification_by", on_delete=models.CASCADE
    )
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    extra_id = models.IntegerField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"[{self.notification_type} | {self.extra_id}]\
            (To '{self.user_to.nickname}' By '{self.user_by.nickname}')"

    class Meta:
        ordering = ["-created"]
