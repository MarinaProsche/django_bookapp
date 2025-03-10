from django.db import models


class Text(models.Model):

    HOME_CITY_TYPE = [
        ('rus', 'Санкт-Петербург'),
        ('eng', 'Saint Petersburg'),
    ]

    chapter_number = models.IntegerField(unique=True)
    title_current_city = models.CharField(max_length=50)
    title_home_city = models.CharField(choices=HOME_CITY_TYPE,max_length=3)
    main_text = models.CharField(max_length=1000)

class MediaFile(models.Model):

    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    file = models.FileField(upload_to='media_files/', blank=True, null=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=5, choices=MEDIA_TYPES)
    

class BuzzWord(models.Model):
    buzzword = models.CharField(max_length=100)
    linked_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, related_name='buzzword_names')

    def __str__(self) -> str:
        return self.buzzword
