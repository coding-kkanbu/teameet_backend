def delete_noti_by_post(sender, instance, created, **kwargs):
    if created:
        pass
    elif instance.is_show is False:
        for postlike in instance.postlike_set.all():
            postlike.notifications.all().delete()
        for postblame in instance.postblame_set.all():
            postblame.notifications.all().delete()


def delete_noti_by_comment(sender, instance, created, **kwargs):
    if created:
        pass
    elif instance.is_show is False:
        instance.notifications.all().delete()
        for commentlike in instance.commentlike_set.all():
            commentlike.notifications.all().delete()
        for commentblame in instance.commentblame_set.all():
            commentblame.notifications.all().delete()
