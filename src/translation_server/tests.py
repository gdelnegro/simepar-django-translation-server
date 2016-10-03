from django.test import TestCase

# Create your tests here.

from .models import *


class TestLastTranslationTag(TestCase):

    def test_translation_tag_is_empty(self):
        """
         If the tag is empty, it should return an empty dict
        """
        last_translation = LastTranslationTag("")
        self.assertEqual(last_translation.return_last_tag(), {'result': {}})

    def test_translation_tag_is_none(self):
        """
         If the tag is empty, it should return an empty dict
        """
        last_translation = LastTranslationTag(None)
        self.assertEqual(last_translation.return_last_tag(), {'result': {}})
