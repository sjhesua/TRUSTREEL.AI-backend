# serializers.py
from rest_framework import serializers
from .models import Video, VideoGenerationQueue, VideoGenerationQueueItem

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video_file', 'uploaded_at']

class VideoGenerationQueueItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoGenerationQueueItem
        fields = ['id', 'videoText','created_at','url','queue']

class VideoGenerationQueueSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = VideoGenerationQueue
        fields = ['id','user','customeURL','videoName', 'created_at', 'items']
    
    def get_items(self, obj):
        items = VideoGenerationQueueItem.objects.filter(queue=obj)
        return VideoGenerationQueueItemSerializer(items, many=True).data