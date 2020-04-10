# Generated by Django 2.2.2 on 2019-06-24 04:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0003_auto_20190622_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partner',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]