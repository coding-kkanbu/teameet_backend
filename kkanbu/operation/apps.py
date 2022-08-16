from django.apps import AppConfig
from django.db.models.signals import pre_delete


class OperationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kkanbu.operation"

    def ready(self):
        from kkanbu.operation import signals

        pre_delete.connect(
            signals.delete_noti_by_postlike,
            sender="operation.PostLike",
            dispatch_uid="delete_noti_by_postlike",
        )
        pre_delete.connect(
            signals.delete_noti_by_commentLike,
            sender="operation.CommentLike",
            dispatch_uid="delete_noti_by_commentlike",
        )
