# Generated by Django 2.2.12 on 2020-05-14 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0004_document_previewurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='downloadUrl',
        ),
        migrations.RemoveField(
            model_name='document',
            name='fileUrl',
        ),
        migrations.RemoveField(
            model_name='document',
            name='previewUrl',
        ),
    ]
