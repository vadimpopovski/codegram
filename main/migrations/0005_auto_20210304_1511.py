# Generated by Django 3.1.4 on 2021-03-04 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_auto_20210213_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloud',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='صاحب'),
        ),
    ]
