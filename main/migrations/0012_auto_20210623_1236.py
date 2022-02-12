# Generated by Django 3.1.7 on 2021-06-23 08:06

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20210618_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='available_views',
        ),
        migrations.AddField(
            model_name='ad',
            name='end_date',
            field=django_jalali.db.models.jDateTimeField(default=django.utils.timezone.now, verbose_name='زمان پایان'),
        ),
    ]