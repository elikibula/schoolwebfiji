# Generated by Django 5.0 on 2025-06-29 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_document_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentcategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, unique=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, unique=True),
        ),
    ]
