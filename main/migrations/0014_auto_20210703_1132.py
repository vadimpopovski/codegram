# Generated by Django 3.1.7 on 2021-07-03 07:02

import datetime
from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20210702_1304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='len_following',
            new_name='len_followings',
        ),
        migrations.RemoveField(
            model_name='person',
            name='following',
        ),
        migrations.AddField(
            model_name='person',
            name='followings',
            field=models.ManyToManyField(blank=True, to='main.Person', verbose_name='دنبال شوندگان'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='end_date',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime(2021, 7, 3, 11, 32, 43, 666013), verbose_name='زمان پایان'),
        ),
    ]
