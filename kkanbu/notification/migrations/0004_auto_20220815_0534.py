# Generated by Django 3.2.11 on 2022-08-14 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_auto_20220302_0244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='sender_content_type',
            new_name='content_type',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='sender_object_id',
            new_name='object_id',
        ),
    ]
