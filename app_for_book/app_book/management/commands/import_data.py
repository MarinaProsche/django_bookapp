import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from app_book.models import Text, BuzzWord, MediaFile


WAY_TO_DATA = os.path.join(settings.BASE_DIR, 'Bookapp.json')

#YOU HAVE TO DELETE db.sqlite file before change something!!!!!!

class Command(BaseCommand):
    help = 'Import from json'


    def add_text_to_base(self, number, text, home_title, current_title, coord):
        text_obj, created = Text.objects.get_or_create(
            chapter_number = number,
            title_current_city = current_title,
            title_home_city='rus' if home_title =='→ Санкт-Петербург, 190000' else 'eng' if home_title =='→ St-Petersburg, 190000' else '',
            main_text=text,
            title_current_city_coord=coord
        )
        return text_obj

    def add_buzzwords_to_base(self, buzzword, linked_file, text_obj):
        buzzword, created = BuzzWord.objects.get_or_create(
            buzzword=buzzword,
            linked_file = linked_file,
            text=text_obj
        )

    def handle(self, *args, **kwargs):
        with open(WAY_TO_DATA, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for chapter in data:
            chapter_number = chapter.get('number', '')
            title_current_city = chapter.get('current_city_title', '')
            title_home_city = chapter.get('home_title', '')
            text = chapter.get('text', '')
            coord = 0.00
            buzzwords = [
                chapter.get('buzzwords-1', ''),
                chapter.get('buzzword-2', ''),
                chapter.get('buzzword-3', '')
            ]

            text_obj = self.add_text_to_base(chapter_number, text, title_home_city, title_current_city, coord)
            for buzzword in buzzwords:
                if buzzword:
                    linked_file = MediaFile.objects.create(
                        file='example.jpg',
                        file_name = 'to be changed',
                        file_type = 'image')
                    self.add_buzzwords_to_base(buzzword=buzzword, linked_file=linked_file, text_obj=text_obj)

        self.stdout.write(self.style.SUCCESS('SUCCESS'))
