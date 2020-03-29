# Generated by Django 2.2.2 on 2019-06-20 07:38

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190620_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.save_image),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='image_thumb',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.save_thumb),
        ),
    ]
