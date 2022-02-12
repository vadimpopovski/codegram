# Generated by Django 3.1.7 on 2021-07-09 07:53

import datetime
from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20210709_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='end_date',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime(2021, 7, 9, 12, 23, 2, 280188), verbose_name='زمان پایان'),
        ),
        migrations.AlterField(
            model_name='person',
            name='liked_posts',
            field=models.ManyToManyField(blank=True, to='main.Post', verbose_name='پسندها'),
        ),
    ]
