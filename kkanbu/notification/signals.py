from django.dispatch import Signal

from kkanbu.notification.models import Notification

notify = Signal()


def notify_handler(sender, message, **kwargs):
    kwargs.pop("signal", None)
    content_obj = sender
    notification = Notification(
        message=str(message), content_object=content_obj, **kwargs
    )
    notification.save()
    return notification


notify.connect(notify_handler, dispatch_uid="notification.models.Notification")
