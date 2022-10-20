# Generated by Django 3.2.11 on 2022-10-20 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20221016_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.CharField(choices=[('20대', 'Twenty'), ('30대', 'Thirty'), ('40대', 'Fourty'), ('50대', 'Fifty'), ('60대', 'Sixty')], max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('남자', 'Male'), ('여자', 'Female')], max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='region',
            field=models.CharField(choices=[('서울', 'Seoul'), ('부산', 'Busan'), ('대구', 'Daegu'), ('인천', 'Incheon'), ('광주', 'Gwangju'), ('대전', 'Daejeon'), ('울산', 'Ulsan'), ('세종', 'Sejong'), ('경기', 'Gyeonggi'), ('강원', 'Gangwon'), ('충북', 'Chungbuk'), ('충남', 'Chungnam'), ('전북', 'Jeonbuk'), ('전남', 'Jeonnam'), ('경북', 'Gyeongbuk'), ('경남', 'Gyeongnam'), ('제주', 'Jeju')], max_length=30),
        ),
    ]
