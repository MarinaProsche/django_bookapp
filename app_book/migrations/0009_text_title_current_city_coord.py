# Generated by Django 5.1.7 on 2025-03-18 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_book', '0008_favorites_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='title_current_city_coord',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
