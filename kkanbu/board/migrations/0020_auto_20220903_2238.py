# Generated by Django 3.2.11 on 2022-09-03 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0019_auto_20220903_2224'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='comment',
            name='comment_length_gte_4',
        ),
        migrations.RemoveConstraint(
            model_name='post',
            name='title_length_gte_4',
        ),
        migrations.RemoveConstraint(
            model_name='post',
            name='content_length_gte_4',
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.CheckConstraint(check=models.Q(('app__in', ['Topic', 'PitAPat'])), name='board_category_app_type_valid'),
        ),
        migrations.AddConstraint(
            model_name='comment',
            constraint=models.CheckConstraint(check=models.Q(('comment__length__gte', 4)), name='board_comment_comment_length_gte_4'),
        ),
        migrations.AddConstraint(
            model_name='post',
            constraint=models.CheckConstraint(check=models.Q(('title__length__gte', 4)), name='board_post_title_length_gte_4'),
        ),
        migrations.AddConstraint(
            model_name='post',
            constraint=models.CheckConstraint(check=models.Q(('content__length__gte', 4)), name='board_post_content_length_gte_4'),
        ),
    ]
