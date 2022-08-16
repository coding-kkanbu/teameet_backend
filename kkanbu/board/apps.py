from django.apps import AppConfig
from django.db.models.signals import post_save


class BoardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kkanbu.board"

    def ready(self):
        from kkanbu.board import signals

        post_save.connect(
            signals.delete_noti_by_post,
            sender="board.Post",
            dispatch_uid="delete_noti_by_post",
        )
        post_save.connect(
            signals.delete_noti_by_comment,
            sender="board.Comment",
            dispatch_uid="delete_noti_by_post",
        )
