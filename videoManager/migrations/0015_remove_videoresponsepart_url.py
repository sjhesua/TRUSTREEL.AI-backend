# Generated by Django 5.1 on 2024-10-21 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videoManager', '0014_alter_videoresponsepart_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoresponsepart',
            name='url',
        ),
    ]
