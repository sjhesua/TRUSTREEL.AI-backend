from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ImageUpload
from .serializers import ImageUploadSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        code = request.POST.get('code')

        if not image or not code:
            return JsonResponse({'error': 'Image and code are required'}, status=400)

        try:
            image_upload = ImageUpload.objects.create(image=image, code=code)
            return JsonResponse({'message': 'Image and code uploaded successfully'}, status=201)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

class ImageUploadListView(APIView):
    def get(self, request, *args, **kwargs):
        images = ImageUpload.objects.all()
        serializer = ImageUploadSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)