# Generated by Django 3.2.11 on 2022-07-09 13:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_nickname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='nickname',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'An address with that email already exists.'}, max_length=254, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='email address'),
        ),
    ]
