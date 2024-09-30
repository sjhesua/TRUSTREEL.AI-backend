from django.contrib import admin
from .models import VideoGenerationQueue, VideoGenerationQueueItem

class VideoGenerationQueueAdmin(admin.ModelAdmin):
    list_display = ('id','videoName', 'user', 'created_at',)
    search_fields = ('user__username',)
    list_filter = ('created_at',)

class VideoGenerationQueueItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'videoText', 'queue', 'status')
    search_fields = ('videoText', 'queue__user__username', 'status')
    list_filter = ('status', 'queue__created_at')

admin.site.register(VideoGenerationQueue, VideoGenerationQueueAdmin)
admin.site.register(VideoGenerationQueueItem, VideoGenerationQueueItemAdmin)