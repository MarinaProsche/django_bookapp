# Generated by Django 5.1.7 on 2025-03-27 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='chapter_cover',
            field=models.FileField(blank=True, null=True, upload_to='media_files/'),
        ),
    ]
