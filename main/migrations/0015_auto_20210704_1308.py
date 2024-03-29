# Generated by Django 3.1.7 on 2021-07-04 08:38

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210703_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='place',
        ),
        migrations.AddField(
            model_name='post',
            name='len_comments',
            field=models.CharField(default='0', max_length=10, verbose_name='تعداد نظر'),
        ),
        migrations.AddField(
            model_name='post',
            name='len_likes',
            field=models.CharField(default='0', max_length=10, verbose_name='تعداد پسند'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='end_date',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime(2021, 7, 4, 13, 8, 0, 449201), verbose_name='زمان پایان'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.post', verbose_name='مطلب'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.person', verbose_name='نویسنده'),
        ),
        migrations.AlterField(
            model_name='file',
            name='cloud',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.cloud', verbose_name='ابر'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='givver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.person', verbose_name='گیرنده'),
        ),
        migrations.AlterField(
            model_name='person',
            name='viewed_posts',
            field=models.ManyToManyField(blank=True, related_name='viewed_posts', to='main.Post', verbose_name='مطالب مشاهده شده'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.person', verbose_name='نویسنده'),
        ),
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, to='main.Comment', verbose_name='نظرات'),
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to='main.Person', verbose_name='پسندیدگان'),
        ),
    ]
