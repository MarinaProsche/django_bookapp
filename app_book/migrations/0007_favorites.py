# Generated by Django 5.1.7 on 2025-03-14 15:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_book', '0006_alter_bookmarks_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorites', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='app_book.mediafile')),
            ],
        ),
    ]
