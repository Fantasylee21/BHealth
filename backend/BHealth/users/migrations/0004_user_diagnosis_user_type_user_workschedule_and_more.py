# Generated by Django 5.1.1 on 2024-09-11 11:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_emailverifyrecord_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='diagnosis',
            field=models.JSONField(blank=True, null=True, verbose_name='诊断记录'),
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('患者', '患者'), ('医生', '医生'), ('药库管理者', '药库管理者')], default='患者', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='workSchedule',
            field=models.JSONField(blank=True, null=True, verbose_name='工作时间表'),
        ),
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 11, 19, 8, 20, 145397), verbose_name='发送时间'),
        ),
    ]
