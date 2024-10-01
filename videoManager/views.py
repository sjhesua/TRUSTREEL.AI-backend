from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, generics
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings

from .models import Video, VideoGenerationQueue, VideoGenerationQueueItem
from .serializers import VideoSerializer,VideoGenerationQueueSerializer, VideoGenerationQueueItemSerializer

import requests
import logging
import os
logger = logging.getLogger(__name__)

class CreateCollection(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Use POST to create a collection'}, status=200)
    
    def post(self, request, *args, **kwargs):
        library_id = request.data.get('library_id')
        name = request.data.get('name')
        #if not library_id:
        #    return Response({'error': 'library_id is required'}, status=400)
        if not name:
            return Response({'error': 'name is required'}, status=400)
        
        #url = f"https://video.bunnycdn.com/library/{library_id}/collections"
        url = "https://video.bunnycdn.com/library/300169/collections"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "AccessKey": "b5d41ba8-20ab-49e7-a04527b9a3dc-bf8b-434b"  # Añade tu AccessKey aquí
        }
        data = {
            "name": name
        }
        
        # Hacer la solicitud a la API de BunnyCDN
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Check for HTTP errors
            return Response(response.json(), status=response.status_code)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - Response content: {response.content}")
            return Response({'error': str(http_err), 'details': response.content.decode()}, status=response.status_code)
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request to BunnyCDN failed: {req_err}")
            return Response({'error': str(req_err)}, status=500)

@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        if not request.content_type.startswith('multipart/form-data'):
            return JsonResponse({'error': 'Unsupported Media Type'}, status=415)

        video_file = request.FILES.get('video')
        if not video_file:
            return JsonResponse({'error': 'No video file provided'}, status=400)

        # Asegurarse de que la ruta de almacenamiento exista
        video_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)

        # Guardar el video en el backend
        video_path = default_storage.save(os.path.join('videos', video_file.name), ContentFile(video_file.read()))
        absolute_video_path = os.path.join(settings.MEDIA_ROOT, video_path)

        # Información de BunnyCDN Storage
        REGION = ''  # Si es la región alemana deja esto como una cadena vacía: ''
        STORAGE_ZONE_NAME = 'video-call-demo'
        ACCESS_KEY = '97033b83-b2dc-4786-9033d399b132-a786-473f'
        FILENAME_EXTENSION = video_file.name

        base_url = "storage.bunnycdn.com"
        if REGION:
            base_url = f"{REGION}.{base_url}"

        url = f"https://{base_url}/{STORAGE_ZONE_NAME}/testfff/{FILENAME_EXTENSION}"

        headers = {
            "AccessKey": ACCESS_KEY,
            "Content-Type": "application/octet-stream",
            "accept": "application/json"
        }

        # Subida del video a BunnyCDN Storage
        try:
            with open(absolute_video_path, 'rb') as file_data:
                response = requests.put(url, headers=headers, data=file_data, verify=False)

            if response.status_code == 201:
                # Eliminar el archivo local después de la subida exitosa
                default_storage.delete(video_path)
                return JsonResponse({'message': 'Video uploaded successfully', 'data': response.json()})
            else:
                # Mantener el archivo local si la subida falla
                return JsonResponse({'error': 'Failed to upload video', 'details': response.text}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error uploading video to BunnyCDN: {e}")
            return JsonResponse({'error': 'Failed to upload video', 'details': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def create_folder(folder_name):
    # Información de BunnyCDN Storage
    REGION = ''  # Si es la región alemana deja esto como una cadena vacía: ''
    STORAGE_ZONE_NAME = 'video-call-demo'
    ACCESS_KEY = '97033b83-b2dc-4786-9033d399b132-a786-473f'

    base_url = "storage.bunnycdn.com"
    if REGION:
        base_url = f"{REGION}.{base_url}"

    folder_url = f"https://{base_url}/{STORAGE_ZONE_NAME}/{folder_name}/"

    headers = {
        "AccessKey": ACCESS_KEY,
        "Content-Type": "application/octet-stream",
        "accept": "application/json"
    }

    # Crear la carpeta en BunnyCDN Storage
    try:
        folder_response = requests.put(folder_url, headers=headers, verify=False)
        if folder_response.status_code in [201, 204]:
            return JsonResponse({'message': 'Folder created successfully'})
        else:
            return JsonResponse({'error': 'Failed to create folder', 'details': folder_response.text}, status=folder_response.status_code)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating folder in BunnyCDN: {e}")
        return JsonResponse({'error': 'Failed to create folder', 'details': str(e)}, status=500)

@csrf_exempt
def create_video(video_name):
    # Información de BunnyCDN Storage
    REGION = ''  # Si es la región alemana deja esto como una cadena vacía: ''
    STORAGE_ZONE_NAME = 'video-call-demo'
    ACCESS_KEY = '97033b83-b2dc-4786-9033d399b132-a786-473f'

    base_url = "storage.bunnycdn.com"
    if REGION:
        base_url = f"{REGION}.{base_url}"

    folder_url = f"https://{base_url}/{STORAGE_ZONE_NAME}/{folder_name}/"

    headers = {
        "AccessKey": ACCESS_KEY,
        "Content-Type": "application/octet-stream",
        "accept": "application/json"
    }

    # Crear la carpeta en BunnyCDN Storage
    try:
        folder_response = requests.put(folder_url, headers=headers, verify=False)
        if folder_response.status_code in [201, 204]:
            return JsonResponse({'message': 'Folder created successfully'})
        else:
            return JsonResponse({'error': 'Failed to create folder', 'details': folder_response.text}, status=folder_response.status_code)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating folder in BunnyCDN: {e}")
        return JsonResponse({'error': 'Failed to create folder', 'details': str(e)}, status=500)


class VideoStream(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateVideoGenerationQueueView(APIView):
    permission_classes = [IsAuthenticated]
    print("XXXXXXXXXXXXXXXXXXXXXXx")
    print("VIDEO CREADO")
    print("XXXXXXXXXXXXXXXXXXXXXXx")
    def post(self, request, *args, **kwargs):
        texts = request.data.get('texts', [])
        replicaCode = request.data['replicaCode']
        videoName = request.data['videoName']
        customeURL = request.data['customeURL']
        
        if not texts:
            return Response({"error": "No texts provided"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        queue = VideoGenerationQueue.objects.create(user=user,replicId=replicaCode,videoName=videoName,customeURL=customeURL)
        items = []
        for text in texts:
            item = VideoGenerationQueueItem(queue=queue, videoText=text)
            item.save()
            items.append(item)

        serializer = VideoGenerationQueueSerializer(queue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VideoGenerationQueueItemListView(generics.ListAPIView):
    serializer_class = VideoGenerationQueueSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return VideoGenerationQueueItem.objects.filter(queue__user_id=user_id)

class VideoGenerationQueueListView(generics.ListAPIView):
    serializer_class = VideoGenerationQueueSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return VideoGenerationQueue.objects.filter(user_id=user_id)

class VideoPorUrl(APIView):
    def get(self, request, *args, **kwargs):
        custome_url = request.query_params.get('customeURL')
        if custome_url is not None:
            queues = VideoGenerationQueue.objects.filter(customeURL=custome_url)
            serializer = VideoGenerationQueueSerializer(queues, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "customeURL parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

#TAVUS
class TavusVideoCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        background_url = request.data.get('background_url', '')
        replica_id = request.data.get('replica_id', '')
        script = request.data.get('script', '')
        video_name = request.data.get('video_name', '')

        if not replica_id or not script or not video_name:
            return Response({"error": "replica_id, script, and video_name are required"}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://tavusapi.com/v2/videos"
        payload = {
            "background_url": background_url,
            "replica_id": replica_id,
            "script": script,
            "video_name": video_name,
            "callback_url":"http://206.1.164.33:8000/videos/tavus/callback/"
        }
        headers = {
            "x-api-key": "<api-key>",  # Reemplaza <api-key> con tu clave API real
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return Response(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def tavus_callback(request):
    # Imprimir el contenido recibido en la consola
    print(request.data)
    # Obtener el video_name y download_url de la solicitud
    video_name = request.data.get('video_name')
    download_url = request.data.get('download_url')
    try:
        # Actualizar el objeto VideoGenerationQueueItem
        video_item = VideoGenerationQueueItem.objects.get(id=video_name)
        video_item.url = download_url
        video_item.save()
        return Response({"message": "URL updated successfully"}, status=status.HTTP_200_OK)
    except VideoGenerationQueueItem.DoesNotExist:
        return Response({"error": "VideoGenerationQueueItem not found"}, status=status.HTTP_404_NOT_FOUND)