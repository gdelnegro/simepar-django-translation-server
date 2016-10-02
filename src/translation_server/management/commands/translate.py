# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 10/1/16.
from django.core.management import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "This command executes all steps for translation"

    app_name = "translation_server"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--copy',
            action='store_true',
            dest='copy_to_project',
            default=False,
            help="Copy the generated *.po and *.mo files to the project's translation dir",
        )

        parser.add_argument(
            '--locales-dir',
            action='store',
            dest='locales_dir',
            default="",
            help="The locales dir to copy the translation files",
        )

    def handle(self, *args, **options):
        call_command('make_translation_migrations')
        call_command('migrate', self.app_name)
        call_command('make_translation', options['copy_to_project'], options['locales_dir'])