# Generated by Django 5.0 on 2025-06-29 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_documentcategory_slug_subcategory_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentcategory',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
