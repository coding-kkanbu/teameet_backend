from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "notification_type",
        "recipient",
        "content_object",
        "is_read",
    )
    list_filter = (
        "notification_type",
        "is_read",
        "created",
    )


admin.site.register(Notification, NotificationAdmin)
