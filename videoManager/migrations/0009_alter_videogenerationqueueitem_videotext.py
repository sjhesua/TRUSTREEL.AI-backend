# Generated by Django 5.1 on 2024-10-01 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoManager', '0008_rename_customurl_videogenerationqueue_customeurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videogenerationqueueitem',
            name='videoText',
            field=models.CharField(max_length=10000),
        ),
    ]