from django.urls import path
from .views import ImageUploadListView

urlpatterns = [
    path('api/images/', ImageUploadListView.as_view(), name='image-upload-list'),
]