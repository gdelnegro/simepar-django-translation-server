# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 21:21:09
from __future__ import unicode_literals

from django.db import migrations


def __load_data(**kwargs):
    apps = kwargs.pop('apps', None)
    if apps:
        translation_type = apps.get_model("translation_server", "TranslationType")
        model = apps.get_model("translation_server", "Translation")
        try:
            mdl = model.objects.get(tag=kwargs['tag'])
        except model.DoesNotExist:
            mdl = model()
        except Exception as err:
            raise err
        for k, v in kwargs.items():
            if k == "type":
                setattr(mdl, k, translation_type.objects.get(tag=v))
            else:
                setattr(mdl, k, v)
        setattr(mdl, "migration_created", True)
        mdl.save()


def clear_data(apps, schema_editor):
    model = apps.get_model("translation_server", "Translation")
    model.objects.filter(tag__in=["MDL12"]).delete()


def load_data(apps, schema_editor):
    __load_data(apps=apps, type="DTSM", tag="MDL12", text="Migration created", text_en="Migration created", text_de="TestDesss", text_pt_br="\"Migration\" criada", auxiliary_tag="TTP12", auxiliary_text="If this record migration was created", auxiliary_text_en="If this record migration was created", auxiliary_text_de="Test", auxiliary_text_pt_br="Se a migration desse registro foi criada", migration_created="True")


class Migration(migrations.Migration):

    dependencies = [
        ('translation_server', '0007_auto_20161004_2113'),
    ]

    operations = [
        migrations.RunPython(load_data, clear_data)
    ]

        