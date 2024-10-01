# models.py
from django.db import models
from company.models import CustomUser

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class VideoGenerationQueue(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    videoName = models.CharField(max_length=100)
    customeURL = models.CharField(max_length=300)
    replicId = models.CharField(max_length=100)

class VideoGenerationQueueItem(models.Model):
    videoText = models.CharField(max_length=10000)
    queue = models.ForeignKey(VideoGenerationQueue, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    url= models.CharField(max_length=100)
    status = models.BooleanField(default=False)