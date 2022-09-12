# Generated by Django 3.2.11 on 2022-09-03 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0018_auto_20220831_2057'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='sogaetingoption',
            name='age_gte_20',
        ),
        migrations.AddConstraint(
            model_name='sogaetingoption',
            constraint=models.CheckConstraint(check=models.Q(('region__in', ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주'])), name='board_sogaetingoption_region_type_valid'),
        ),
        migrations.AddConstraint(
            model_name='sogaetingoption',
            constraint=models.CheckConstraint(check=models.Q(('gender__in', [1, 2])), name='board_sogaetingoption_gender_type_valid'),
        ),
        migrations.AddConstraint(
            model_name='sogaetingoption',
            constraint=models.CheckConstraint(check=models.Q(('age__gte', 20)), name='board_sogaetingoption_age_gte_20'),
        ),
    ]
