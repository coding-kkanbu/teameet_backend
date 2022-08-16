from django.contrib.contenttypes.models import ContentType

from kkanbu.notification.models import Notification


def delete_noti_by_postlike(sender, instance, **kwargs):
    ctype = ContentType.objects.get_for_model(instance)
    Notification.objects.filter(content_type=ctype, object_id=instance.pk).delete()


def delete_noti_by_commentLike(sender, instance, **kwargs):
    ctype = ContentType.objects.get_for_model(instance)
    Notification.objects.filter(content_type=ctype, object_id=instance.pk).delete()
