from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from translation_server.models import *
from django.urls.exceptions import NoReverseMatch


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
            self.assertEqual(reverse_error, True)

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
            self.assertEqual(reverse_error, False)

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
