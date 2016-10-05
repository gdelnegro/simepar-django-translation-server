# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translation_server', '0004_auto_20161002_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='auxiliary_text_de',
            field=models.TextField(blank=True, help_text='TTP11', null=True, verbose_name='MDL11'),
        ),
        migrations.AddField(
            model_name='translation',
            name='text_de',
            field=models.TextField(help_text='TTP9', null=True, verbose_name='MDL9'),
        ),
        migrations.AddField(
            model_name='translationtype',
            name='name_de',
            field=models.TextField(help_text='TTP4', null=True, verbose_name='MDL4'),
        ),
    ]
