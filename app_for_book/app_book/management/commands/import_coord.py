import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from app_book.models import Text


WAY_TO_DATA = os.path.join(settings.BASE_DIR, 'Bookapp.json')

class Command(BaseCommand):
    help = 'Import map from json'

    def handle(self, *args, **kwargs):
        with open(WAY_TO_DATA, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for chapter in data:
            number = chapter.get('number', '')
            coord = chapter.get('coord')
            current_text = Text.objects.get(chapter_number = number)
            current_text.title_current_city_coord = coord if coord else 0.0
            current_text.save()

        self.stdout.write(self.style.SUCCESS('SUCCESS'))
