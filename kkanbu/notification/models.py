from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.timesince import timesince
from django_extensions.db.models import TimeStampedModel

User = settings.AUTH_USER_MODEL


class Notification(TimeStampedModel):
    class NotiType(models.TextChoices):
        COMMENT = "comment"
        POSTLIKE = "postlike"
        COMMENTLIKE = "commentlike"
        POSTBLAME = "postblame"
        COMMENTBLAME = "commentblame"

    notification_type = models.CharField(max_length=20, choices=NotiType.choices)
    # notification(을 만드는)과 연결된 객체
    content_type = models.ForeignKey(
        ContentType, related_name="notify_sender", on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    # sender를 content_object로 이름 변경
    content_object = GenericForeignKey("content_type", "object_id")
    recipient = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    # notification의 내용
    # (ex. 댓글이 달렸습니다 / 좋아요를 받았습니다 / 계정이 인증되었습니다)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False, blank=False, db_index=True)

    class Meta:
        ordering = ("-created",)
        index_together = (
            "recipient",
            "is_read",
        )

    def timesince(self, now=None):
        return timesince(self.created, now)

    def __str__(self):
        return f"[{self.id}] {self.message} {self.timesince()} ago"

    def get_absolute_url(self):
        try:
            if self.notification_type == "comment":
                return reverse("api:Comment-detail", args=[self.content_object.pk])
            elif self.notification_type in ["commentlike", "commentblame"]:
                return reverse(
                    "api:Comment-detail", args=[self.content_object.comment.pk]
                )
            else:
                app = self.content_object.post.category.app
                if app == "Topic":
                    return reverse(
                        "api:Topic-detail", args=[self.content_object.post.pk]
                    )
                if app == "PitAPat":
                    return reverse(
                        "api:PitAPat-detail", args=[self.content_object.post.pk]
                    )
        except Exception as e:
            return e
