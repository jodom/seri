# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-19 05:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0002_auto_20180118_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serie',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]