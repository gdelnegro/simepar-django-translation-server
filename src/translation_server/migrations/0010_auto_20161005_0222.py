# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-05 02:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translation_server', '0009_auto_20161005_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translationtype',
            name='auxiliary_tag',
            field=models.CharField(blank=True, default=False, help_text='DTST6', max_length=20, unique=True, verbose_name='DTSM6'),
        ),
    ]
