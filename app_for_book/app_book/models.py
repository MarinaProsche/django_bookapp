from django.db import models
from django.contrib.auth.models import User


class Text(models.Model):

    HOME_CITY_TYPE = [
        ('rus', 'Санкт-Петербург'),
        ('eng', 'Saint Petersburg'),
    ]

    chapter_number = models.IntegerField(primary_key=True)
    title_current_city = models.CharField(max_length=50, blank=True, null=True)
    title_current_city_coord = models.CharField(max_length=100)
    title_home_city = models.CharField(choices=HOME_CITY_TYPE,max_length=3)
    main_text = models.CharField(max_length=5000)
    chapter_cover = models.FileField(upload_to='media_files/')

    @property
    def has_bookmark(self):
        return Bookmarks.objects.filter(bookmark=self).exists()

class MediaFile(models.Model):

    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    file = models.FileField(upload_to='media_files/', blank=True, null=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=5, choices=MEDIA_TYPES)

    @property
    def link_to_image(self):
        return self.file.url if self.file else None 

class BuzzWord(models.Model):
    buzzword = models.CharField(max_length=100)
    linked_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, to_field='chapter_number', related_name='buzzword_names')

    def __str__(self) -> str:
        return self.buzzword

class Bookmarks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookmark = models.ForeignKey(Text, on_delete=models.CASCADE, to_field='chapter_number', related_name='bookmark')

class Favorites(models.Model):
    user = user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorites = models.ForeignKey(MediaFile, on_delete=models.CASCADE, related_name = 'favorites')

    # class Meta:
    #     unique_together = ('user', 'bookmark')
