from django.core.management.base import BaseCommand, CommandError
from ...languages import LANGUAGES as languages
import os, json

class Command(BaseCommand):
    help = 'Create fixtures for language'

    def handle(self, *args, **options):

        json_data = []

        _pk = 1

        for language_item in languages:
            language_code = language_item[0]
            language_name = "%s" % language_item[1]

            json_item = {
                "model": "provider.language",
                "pk": _pk,
                "fields": {
                    "code": language_code,
                    "name": language_name
                }
            }

            json_data.append(json_item)

            _pk += 1

        dir = '%s/../../fixtures/' % os.path.dirname(os.path.abspath(__file__))
        json_file = '%s/languages.json' % dir
        with open(json_file, 'w') as fp:
            json.dump(json_data, fp)