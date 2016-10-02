# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 9/30/16.
from django import forms
from django.utils.translation import ugettext_lazy as _
from translation_server.models import *


class TranslationAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(TranslationAdminForm, self).clean()
        auxiliary_text_en = cleaned_data.get("auxiliary_text_en")
        primary_text_en = cleaned_data.get("text_en")
        auxiliary_text_pt_br = cleaned_data.get("auxiliary_text_pt_br")
        primary_text_pt_br = cleaned_data.get("text_pt_br")

        if auxiliary_text_en == primary_text_en:
            self.add_error('auxiliary_text_en', forms.ValidationError(_('ME1'), code='identical_texts_en'))
        if auxiliary_text_pt_br == primary_text_pt_br:
            self.add_error('auxiliary_text_pt_br', forms.ValidationError(_('ME1'), code='identical_texts_pt_br'))

        return cleaned_data

    def save(self, commit=False):
        translation = super(TranslationAdminForm, self).save(commit=commit)
        translation.save()
        translation.migration_created = False
        translation.save()
        return translation

    class Meta:
        model = Translation
        fields = "__all__"