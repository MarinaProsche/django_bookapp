from django.contrib import admin

from .models import BuzzWord, Text, MediaFile

@admin.register(BuzzWord)
class BuzzWordAdmin(admin.ModelAdmin):
    list_display = ('text', 'buzzword', 'linked_file')


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('chapter_number', 'title_current_city', 'title_current_city_coord', 'title_home_city', 'main_text', 'buzzwords')


    def buzzwords(self, obj):
        return ', '.join([buzzword.buzzword for buzzword in obj.buzzword_names.all()])
    
    buzzwords.short_description = 'Buzzwords'


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'file_name', 'file_type', 'buzzwords')

    def buzzwords(self, obj):
        return ', '.join([buzzword.buzzword for buzzword in obj.buzzword_set.all()])
    buzzwords.short_description = 'Buzzwords'
