# Generated by Django 3.2.11 on 2022-07-31 07:10

from django.db import migrations, models
import kkanbu.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_introduce'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=kkanbu.users.models.profile_image_file_path, verbose_name='profile'),
        ),
    ]
