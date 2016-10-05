from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from translation_server.models import *
from django.urls.exceptions import NoReverseMatch
from django.apps import *
from translation_server.forms import *


class TestLastTranslationTagModel(TestCase):

    def test_translation_tag_is_empty(self):
        """
         If the tag is empty, it should return an empty dict
        """
        last_translation = LastTranslationTag("")
        self.assertEqual(last_translation.return_last_tag(), {'result': {}})

    def test_translation_tag_is_none(self):
        """
         If the tag is None, it should return an empty dict
        """
        last_translation = LastTranslationTag(None)
        self.assertEqual(last_translation.return_last_tag(), {'result': {}})

    def test_translation_tag_exists(self):
        """
         If the tag exists, it should return a dict with the key last_id
        """
        last_translation = LastTranslationTag('MDL1')
        self.assertIn('last_id', last_translation.return_last_tag()['result'])

    def test_translation_tag_does_not_exists(self):
        """
         If the tag does not exists, it should return an empty dict
        """
        last_translation = LastTranslationTag('MDL66')
        self.assertNotIn('last_id', last_translation.return_last_tag()['result'])


class TestLastTranslationTagView(APITestCase):

    def test_post_with_id_in_url(self):
        try:
            url = reverse('get_last_translation_tag', args=[TranslationType.objects.get(tag="MDL").id])
            print(url)
        except Exception as error:
            raise error
        else:
            response = self.client.post(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_with_id_in_url(self):
        try:
            url = reverse('get_last_translation_tag', args=[TranslationType.objects.get(tag="MDL").id])
        except Exception as error:
            raise error
        else:
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("last_id", response.data['result'])

    def test_get_with_empty_tag(self):
        reverse_error = False
        try:
            url = reverse('get_last_translation_tag', args=[""])
        except NoReverseMatch:
            reverse_error = True
        except Exception as error:
            raise error
        else:
            self.assertTrue(reverse_error)

    def test_get_with_tag_equal_none(self):
        reverse_error = False
        try:
            url = reverse('get_last_translation_tag', args=[None])
        except NoReverseMatch:
            reverse_error = True
        except Exception as error:
            raise error
        else:
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertFalse(reverse_error)

    def test_get_with_tag_that_exists(self):
        try:
            url = reverse('get_last_translation_tag', args=[TranslationType.objects.get(tag="MDL").tag])
        except Exception as error:
            raise error
        else:
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("last_id", response.data['result'])

    def test_get_with_tag_that_does_not_exist(self):
        try:
            url = reverse('get_last_translation_tag', args=["TEST"])
        except Exception as error:
            raise error
        else:
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestTranslationTypeForm(TestCase):
    def translation_type_creation_without_auxiliary_tag(self):
        fields_to_ignore = ['id', 'created_at', 'updated_at', 'translation_translation_type']
        model_fields = [field.name if field.name not in fields_to_ignore else None for field in
                        apps.get_model('translation_server', "TranslationType")._meta.get_fields()]
        form_data = {}
        for field in model_fields:
            if field:
                if field == 'has_auxiliary_text':
                    value = False
                if field == 'auxiliary_tag':
                    value = ""
                else:
                    value = field.upper()
                form_data.update({field: value})
        form = TranslationTypeAdminForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def translation_type_creation_with_auxiliary_tag(self):
        fields_to_ignore = ['id', 'created_at', 'updated_at', 'translation_translation_type']
        model_fields = [field.name if field.name not in fields_to_ignore else None for field in
                        apps.get_model('translation_server', "TranslationType")._meta.get_fields()]
        form_data = {}
        for field in model_fields:
            if field:
                if field == 'has_auxiliary_text':
                    value = True
                if field == 'auxiliary_tag':
                    value = "AUX"
                else:
                    value = field.upper()
                form_data.update({field: value})
        form = TranslationTypeAdminForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())


class TestTranslationForm(TestCase):
    def translation_MDL_creation(self):
        languages_list = [lang[0].replace('-', '_') for lang in settings.LANGUAGES]
        fields_to_ignore = ['id', 'created_at', 'updated_at', 'translation_translation_type']
        model_fields = [field.name if field.name not in fields_to_ignore else None for field in
                        apps.get_model('translation_server', "Translation")._meta.get_fields()]
        form_data = {}
        translation_type_object = TranslationType.objects.get(tag="MDL")
        for language in languages_list:
            form_data.update({"text_"+language: "TEST"})
            if translation_type_object.has_auxiliary_text:
                form_data.update({"auxiliary_text_" + language: "TEST"})
        model_fields.pop(model_fields.index("text"))
        model_fields.pop(model_fields.index("auxiliary_text"))
        for field in model_fields:
            if field:
                if field == "type":
                    value = translation_type_object
                if field == 'tag':
                    value = translation_type_object.tag + 1
                if field == "auxiliary_tag":
                    value = translation_type_object.auxiliary_tag + 1 if translation_type_object.has_auxiliary_text else ""
                else:
                    value = field.upper()
                form_data.update({field: value})
        form = TranslationAdminForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def translation_MTA_creation(self):
        languages_list = [lang[0].replace('-', '_') for lang in settings.LANGUAGES]
        fields_to_ignore = ['id', 'created_at', 'updated_at', 'translation_translation_type']
        model_fields = [field.name if field.name not in fields_to_ignore else None for field in
                        apps.get_model('translation_server', "Translation")._meta.get_fields()]
        form_data = {}
        translation_type_object = TranslationType.objects.get(tag="MTA")
        for language in languages_list:
            form_data.update({"text_" + language: "TEST"})
            if translation_type_object.has_auxiliary_text:
                form_data.update({"auxiliary_text_" + language: "TEST"})
        model_fields.pop(model_fields.index("text"))
        model_fields.pop(model_fields.index("auxiliary_text"))
        for field in model_fields:
            if field:
                if field == "type":
                    value = translation_type_object
                if field == 'tag':
                    value = translation_type_object.tag + 1
                if field == "auxiliary_tag":
                    value = translation_type_object.auxiliary_tag + 1 if translation_type_object.has_auxiliary_text else ""
                else:
                    value = field.upper()
                form_data.update({field: value})
        form = TranslationAdminForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def translation_ME_creation(self):
        languages_list = [lang[0].replace('-', '_') for lang in settings.LANGUAGES]
        fields_to_ignore = ['id', 'created_at', 'updated_at', 'translation_translation_type']
        model_fields = [field.name if field.name not in fields_to_ignore else None for field in
                        apps.get_model('translation_server', "Translation")._meta.get_fields()]
        form_data = {}
        translation_type_object = TranslationType.objects.get(tag="ME")
        for language in languages_list:
            form_data.update({"text_" + language: "TEST"})
            if translation_type_object.has_auxiliary_text:
                form_data.update({"auxiliary_text_" + language: "TEST"})
        model_fields.pop(model_fields.index("text"))
        model_fields.pop(model_fields.index("auxiliary_text"))
        for field in model_fields:
            if field:
                if field == "type":
                    value = translation_type_object
                if field == 'tag':
                    value = translation_type_object.tag + 1
                if field == "auxiliary_tag":
                    value = translation_type_object.auxiliary_tag + 1 if translation_type_object.has_auxiliary_text else ""
                else:
                    value = field.upper()
                form_data.update({field: value})
        form = TranslationAdminForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def translation_GEN_creation(self):
        languages_list = [lang[0].replace('-', '_') for lang in settings.LANGUAGES]
        fields_to_ignore = ['id', 'created_at', 'updated_at', 'translation_translation_type']
        model_fields = [field.name if field.name not in fields_to_ignore else None for field in
                        apps.get_model('translation_server', "Translation")._meta.get_fields()]
        form_data = {}
        translation_type_object = TranslationType.objects.get(tag="GEN")
        for language in languages_list:
            form_data.update({"text_" + language: "TEST"})
            if translation_type_object.has_auxiliary_text:
                form_data.update({"auxiliary_text_" + language: "TEST"})
        model_fields.pop(model_fields.index("text"))
        model_fields.pop(model_fields.index("auxiliary_text"))
        for field in model_fields:
            if field:
                if field == "type":
                    value = translation_type_object
                if field == 'tag':
                    value = translation_type_object.tag + 1
                if field == "auxiliary_tag":
                    value = translation_type_object.auxiliary_tag + 1 if translation_type_object.has_auxiliary_text else ""
                else:
                    value = field.upper()
                form_data.update({field: value})
        form = TranslationAdminForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
