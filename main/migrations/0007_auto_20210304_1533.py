# Generated by Django 3.1.4 on 2021-03-04 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]