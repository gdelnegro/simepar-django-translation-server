# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 10/1/16.
from django.core.management import BaseCommand
from django.conf import settings
from datetime import datetime
from translation_server.models import Translation
from django.core.management import call_command


class Command(BaseCommand):
    help = "This command generates the translation files, based on the contents of 'Translation' model"

    @staticmethod
    def __create_translation_files():
        dir_en_us = settings.BASE_DIR + '/locale/en/LC_MESSAGES/'
        dir_pt_br = settings.BASE_DIR + '/locale/pt_BR/LC_MESSAGES/'
        file_en_us = open(dir_en_us + "django.po", "w+")
        file_pt_br = open(dir_pt_br + "django.po", "w+")
        header = """
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2016-05-19 14:44+0000\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"Language: \\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n > 1);\\n"
"""

        try:
            file_pt_br.write("%s# Aquivo gerado em: %s \n\n" % (header, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            file_en_us.write("%s# File generated in: %s \n\n" % (header, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            for obj in Translation.objects.filter():
                file_en_us.write('msgid "%s"\nmsgstr "%s"\n\n' % (obj.tag, obj.text_en))
                file_pt_br.write('msgid "%s"\nmsgstr "%s"\n\n' % (obj.tag, obj.text_pt_br))
                if obj.type.has_auxiliary_text:
                    file_en_us.write('msgid "%s"\nmsgstr "%s"\n\n' % (obj.auxiliary_tag, obj.auxiliary_text_en))
                    file_pt_br.write('msgid "%s"\nmsgstr "%s"\n\n' % (obj.auxiliary_tag, obj.auxiliary_text_pt_br))
        except Exception as error:
            file_en_us.close()
            file_pt_br.close()
            raise error
        else:
            file_en_us.close()
            file_pt_br.close()
            return True

    def handle(self, *args, **options):
        if self.__create_translation_files():
            call_command('compilemessages')
