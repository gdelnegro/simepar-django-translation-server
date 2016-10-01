# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 10/1/16.
from django.core.management import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "This command executes all steps for translation"

    def handle(self, *args, **options):
        call_command('make_translation_migrations')
        call_command('migrate', 'portfolio')
        call_command('make_translation')