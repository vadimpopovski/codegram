# Generated by Django 3.1.7 on 2021-07-09 06:50

import datetime
from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20210707_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='end_date',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime(2021, 7, 9, 11, 20, 24, 883317), verbose_name='زمان پایان'),
        ),
    ]
