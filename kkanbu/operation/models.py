from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from kkanbu.board.models import Comment, Post
from kkanbu.notification.models import Notification

User = settings.AUTH_USER_MODEL


class PostLike(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notifications = GenericRelation(Notification)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["post", "user"],
                name="unique_postlike",
            )
        ]

    def __str__(self):
        return f"{self.post} liked by {self.user}"

    def get_absolute_url(self):
        app = self.post.category.app
        if app == "Topic":
            return reverse("api:Topic-detail", kwargs={"pk": self.post.pk})
        elif app == "PitAPat":
            return reverse("api:PitAPat-detail", kwargs={"pk": self.post.pk})
        else:
            return None


@receiver(pre_delete, sender=PostLike)
def delete_noti_by_postlike(sender, instance, **kwargs):
    ctype = ContentType.objects.get_for_model(instance)
    Notification.objects.filter(content_type=ctype, object_id=instance.pk).delete()


class CommentLike(TimeStampedModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notifications = GenericRelation(Notification)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["comment", "user"],
                name="unique_commentlike",
            )
        ]

    def __str__(self):
        return f"{self.comment} liked by {self.user}"

    def get_absolute_url(self):
        return reverse("api:Comment-detail", kwargs={"pk": self.comment.pk})


@receiver(pre_delete, sender=CommentLike)
def delete_noti_by_commentLike(sender, instance, **kwargs):
    ctype = ContentType.objects.get_for_model(instance)
    Notification.objects.filter(content_type=ctype, object_id=instance.pk).delete()


# Blame Reason Category
class ReasonType(models.TextChoices):
    ABUSE = "abuse", _("욕설")
    DEFAME = "defame", _("비방")
    SPAM = "spam", _("도배")
    FALSEFACT = "falsefact", _("허위사실")
    ADVERTISE = "advertise", _("광고")
    INCORRECT = "incorrect", _("게시판미부합")
    ETC = "etc", _("기타사항")


class PostBlame(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(
        max_length=30, choices=ReasonType.choices, default=ReasonType.ETC
    )
    description = models.TextField(null=True, blank=True)
    notifications = GenericRelation(Notification)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["post", "user"], name="unique_postblame"),
        ]

    def __str__(self):
        return f"{self.post} blamed by {self.user} for reason {self.reason}"

    def get_absolute_url(self):
        app = self.post.category.app
        if app == "Topic":
            return reverse("api:Topic-detail", kwargs={"pk": self.post.pk})
        elif app == "PitAPat":
            return reverse("api:PitAPat-detail", kwargs={"pk": self.post.pk})
        else:
            return None


class CommentBlame(TimeStampedModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(
        max_length=30, choices=ReasonType.choices, default=ReasonType.ETC
    )
    description = models.TextField(null=True, blank=True)
    notifications = GenericRelation(Notification)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["comment", "user"], name="unique_commentblame"),
        ]

    def __str__(self):
        return f"{self.comment} blamed by {self.user} for reason {self.reason}"

    def get_absolute_url(self):
        return reverse("api:Comment-detail", kwargs={"pk": self.comment.pk})
