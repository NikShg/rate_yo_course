# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-08 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rateYoCourse', '0005_university_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='university',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
