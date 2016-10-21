# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 19:45
from __future__ import unicode_literals

from django.db import migrations


def __load_data(**kwargs):
    apps = kwargs.pop('apps', None)
    if apps:
        model = apps.get_model("translation_server", "TranslationType")
        try:
            mdl = model.objects.get(tag=kwargs['tag'])
        except model.DoesNotExist:
            mdl = model()
        except Exception as err:
            raise err
        for k, v in kwargs.items():
            setattr(mdl, k, v)
        mdl.save()


def load_data(apps, schema_editor):
    __load_data(apps=apps, tag='DTSM', name_pt_br="Modelo", name_en="Model", has_auxiliary_text=True,
                auxiliary_tag="DTST")
    __load_data(apps=apps, tag='DTSMT', name_pt_br="Meta", name_en="Meta", has_auxiliary_text=True,
                auxiliary_tag="DTSMTP")
    __load_data(apps=apps, tag='DTSG', name_pt_br="Texto", name_en="General Text", has_auxiliary_text=False,
                auxiliary_tag="GTP")
    __load_data(apps=apps, tag='DTSE', name_pt_br="Mensagem de erro", name_en="Error message", has_auxiliary_text=False,
                auxiliary_tag="MEE")


def revert_data(apps, schema_editor):
    model = apps.get_model("translation_server", "TranslationType")
    model.objects.filter(tag__in=["DTSM", "DTSMT", "DTSG", "DTSE"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('translation_server', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data, revert_data)
    ]
