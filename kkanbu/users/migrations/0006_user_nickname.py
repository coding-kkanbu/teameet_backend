# Generated by Django 3.2.10 on 2022-01-18 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_random_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='teameet', max_length=150, unique=True, verbose_name='nickname'),
            preserve_default=False,
        ),
    ]
