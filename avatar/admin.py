from django.contrib import admin
from .models import ImageUpload

class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'replicaName' ,'code', 'uploaded_at')
    search_fields = ('code',)
    list_filter = ('uploaded_at',)

admin.site.register(ImageUpload, ImageUploadAdmin)