from django.contrib import admin
from .models import VideoGenerationQueue, VideoGenerationQueueItem, VideoResponse, VideoResponsePart

class VideoGenerationQueueAdmin(admin.ModelAdmin):
    list_display = ('id','videoName', 'user', 'created_at',)
    search_fields = ('user__username',)
    list_filter = ('created_at','videoName',)
    

class VideoGenerationQueueItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'videoText', 'queue', 'status')
    search_fields = ('videoText', 'queue__user__username', 'status')
    list_filter = ('status', 'queue__created_at')

class VideoResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'user', 'created_at', 'status')
    search_fields = ('video__videoName', 'user__username', 'status')
    list_filter = ('status', 'created_at')

class VideoResponsePartAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'url', 'created_at', 'status')
    search_fields = ('video__videoName', 'url', 'status')
    list_filter = ('status', 'created_at')

admin.site.register(VideoResponse)
admin.site.register(VideoResponsePart)

admin.site.register(VideoGenerationQueue, VideoGenerationQueueAdmin)
admin.site.register(VideoGenerationQueueItem, VideoGenerationQueueItemAdmin)