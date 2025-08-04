# https://drive.google.com/file/d/1tOHzYekKL9VARhUJ9n2zD7lLQNDp5bpi/view?usp=sharing"

# "https://drive.google.com/thumbnail?id=1tOHzYekKL9VARhUJ9n2zD7lLQNDp5bpi"

import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from app_book.models import Text, BuzzWord, MediaFile
import re
from django.core.files import File

# def convert_drive_link(link):
#     match = re.search(r'/d/([^/]+)/', link)
#     if match:
#         file_id = match.group(1)
#         return f"https://drive.google.com/thumbnail?id={file_id}"
#     return link


WAY_TO_DATA = os.path.join(settings.BASE_DIR, 'Bookapp.json')

class Command(BaseCommand):
    help = 'Import pictures from json'

    def handle(self, *args, **kwargs):
        with open(WAY_TO_DATA, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for chapter in data:
            number = chapter.get('number', '')
            pictures = [chapter.get('picture-1'),
                       chapter.get('picture-2'),
                       chapter.get('picture-3'),
                    #    chapter.get('картинки-4')
                       ]

            pictures = [picture for picture in pictures if picture]
            current_buzzwords = BuzzWord.objects.filter(text__chapter_number=number)

            if current_buzzwords.exists():
                for buzzword, picture in zip(current_buzzwords, pictures):
                    if picture:
                        file_path = os.path.join(settings.MEDIA_ROOT, picture)
                        if os.path.exists(file_path):
                            with open(file_path, 'rb') as f:
                                file_obj = File(f)
                                file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]
                                ext = os.path.splitext(file_path)[1].lower()
                                file_type = "video" if ext == ".mp4" else "image"
                                linked_file = buzzword.linked_file
                                linked_file.file.save(os.path.basename(file_path), file_obj, save=False)

                                linked_file.file_name = file_name_without_ext
                                linked_file.file_type = file_type

                                linked_file.save()
        self.stdout.write(self.style.SUCCESS('SUCCESS'))
