# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 23:25:11
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
    model.objects.filter(tag__in=["MDL2", "MDL3", "MDL4", "MDL6", "MDL5", "MTA1", "MDL1"]).delete()


def load_data(apps, schema_editor):
    __load_data(apps=apps, tag="MDL2", type="MDL", text_pt_br="Atualizado em", text_en="Updated at", auxiliary_tag="TTP2", auxiliary_text_pt_br="Data de atualização do registro", auxiliary_text_en="Record update time")
    __load_data(apps=apps, tag="MDL3", type="MDL", text_pt_br="Tag", text_en="Tag", auxiliary_tag="TTP3", auxiliary_text_pt_br="Identificador único que será usado como prefixo da tag das traduções", auxiliary_text_en="Unique identifier that will be used as prefix for the translations tag")
    __load_data(apps=apps, tag="MDL4", type="MDL", text_pt_br="Nome", text_en="Name", auxiliary_tag="TTP4", auxiliary_text_pt_br="Nome do registro", auxiliary_text_en="Record name")
    __load_data(apps=apps, tag="MDL6", type="MDL", text_pt_br="Tag do texto auxiliar", text_en="Auxiliary text tag", auxiliary_tag="TTP5", auxiliary_text_pt_br="O prefixo para o  identificador único do texto auxiliar", auxiliary_text_en="The unique identifier prefix for auxiliary text")
    __load_data(apps=apps, tag="MDL5", type="MDL", text_pt_br="Tem texto auxiliar?", text_en="Has auxiliary text?", auxiliary_tag="TTP7", auxiliary_text_pt_br="Se o tipo de tradução tem texto auxiliar", auxiliary_text_en="If the translation type have auxiliary text")
    __load_data(apps=apps, tag="MTA1", type="MTA", text_pt_br="Tipo de tradução", text_en="Translation Type", auxiliary_tag="MTP1", auxiliary_text_pt_br="Tipos de tradução", auxiliary_text_en="Translation Types")
    __load_data(apps=apps, tag="MDL1", type="MDL", text_pt_br="Criado em", text_en="Created at", auxiliary_tag="TTP1", auxiliary_text_pt_br="Data de criação do registro", auxiliary_text_en="Record creation date")


class Migration(migrations.Migration):

    dependencies = [
        ('translation_server', '0002_auto_20161001_1945'),
    ]

    operations = [
        migrations.RunPython(load_data, clear_data)
    ]

        