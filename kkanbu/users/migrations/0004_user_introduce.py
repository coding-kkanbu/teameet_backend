# Generated by Django 3.2.11 on 2022-07-27 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220709_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='introduce',
            field=models.TextField(blank=True, null=True, verbose_name='introduce'),
        ),
    ]
