# Generated by Django 2.2.12 on 2020-05-13 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

<<<<<<< HEAD
    dependencies = [("asset", "0002_auto_20200513_2109")]

    operations = [
        migrations.AddField(
            model_name="document", name="downloadUrl", field=models.URLField(blank=True)
        )
=======
    dependencies = [
        ("asset", "0002_auto_20200513_2109"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="downloadUrl",
            field=models.URLField(blank=True),
        ),
>>>>>>> 12cc8a162119b10802d20e23ccc52bc98341a975
    ]
