# Generated by Django 5.1 on 2024-09-24 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoManager', '0005_videogenerationqueueitem_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='videogenerationqueue',
            name='videoName',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
