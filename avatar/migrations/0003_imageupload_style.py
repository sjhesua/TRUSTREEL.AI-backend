# Generated by Django 5.1 on 2024-10-03 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avatar', '0002_imageupload_replicaname'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageupload',
            name='style',
            field=models.CharField(default='', max_length=1000),
        ),
    ]