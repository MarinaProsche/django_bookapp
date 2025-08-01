import os
import re
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from app_book.models import Text


WAY_TO_DATA = os.path.join(settings.BASE_DIR, 'Bookapp.json')


def convert_drive_link(link):
    match = re.search(r'/d/([^/]+)/', link)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/thumbnail?id={file_id}&s=150"
    return link

class Command(BaseCommand):
    help = 'Import picture with number from json'

    def handle(self, *args, **kwargs):
        with open(WAY_TO_DATA, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for chapter in data:
            number = chapter.get('number', '')
            pic_with_number = chapter.get('картинки с номерам')
            current_text = Text.objects.get(chapter_number = number)
            current_text.chapter_cover = convert_drive_link(str(pic_with_number))
            current_text.save()

        self.stdout.write(self.style.SUCCESS('SUCCESS'))
