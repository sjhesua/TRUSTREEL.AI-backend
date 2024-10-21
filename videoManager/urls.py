from django.urls import path
from django.conf import settings
from . import views
from .views import CreateCollection,VideoPorUrl,VideoGenerationQueueListView,VideoStream,VideoGenerationQueueItemListView, upload_video, CreateVideoGenerationQueueView,tavus_callback
from .views import create_video_response, create_video_response_part
from django.conf.urls.static import static

urlpatterns = [
    path('api/create_collection/', CreateCollection.as_view(), name='create-collection'),
    path('api/upload/', VideoStream.as_view(), name='video-upload'),
    path('upload-video/', upload_video, name='upload_video'),
    path('api/video-generation-queue/', CreateVideoGenerationQueueView.as_view(), name='create_video_generation_queue'),
    path('video-generation-queues/user/', VideoGenerationQueueListView.as_view(), name='video-generation-queue-list'),
    path('video-generation-queue-items/user/<int:user_id>/', VideoGenerationQueueItemListView.as_view(), name='video-generation-queue-item-list'),
    
    path('create-video-response/', create_video_response, name='create_video_response'),
    path('create-video-response-part/', create_video_response_part, name='create_video_response_part'),

    path('app/viedo-url', VideoPorUrl.as_view(), name='video-url'),
    path('tavus/callback/', tavus_callback, name='tavus_callback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)