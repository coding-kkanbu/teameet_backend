from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timesince import timesince
from django_extensions.db.models import TimeStampedModel

from .signals import notify

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
    sender_content_type = models.ForeignKey(
        ContentType, related_name="notify_sender", on_delete=models.CASCADE
    )
    sender_object_id = models.PositiveIntegerField()
    sender = GenericForeignKey("sender_content_type", "sender_object_id")
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

    def get_absolute_url(self):
        if self.notification_type in ["commentlike", "commentblame"]:
            return "/api/v1/comment/%d/" % self.sender.comment.pk
        else:
            return "/api/v1/post/%d/" % self.sender.post.pk


def notify_handler(message, **kwargs):
    kwargs.pop("signal", None)
    sender = kwargs.pop("sender")
    recipient = kwargs.pop("recipient")
    noti_type = kwargs.pop("noti_type")

    notify = Notification(
        notification_type=noti_type,
        sender=sender,
        recipient=recipient,
        message=str(message),
    )
    notify.save()

    return notify


notify.connect(notify_handler, dispatch_uid="notification.models.Notification")
