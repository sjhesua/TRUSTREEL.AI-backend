# Generated by Django 5.1 on 2024-10-21 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoManager', '0013_remove_videoresponse_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoresponsepart',
            name='url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]