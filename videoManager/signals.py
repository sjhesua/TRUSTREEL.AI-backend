import requests
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import VideoGenerationQueueItem
from dotenv import load_dotenv

load_dotenv()

@receiver(post_save, sender=VideoGenerationQueueItem)
def create_video_on_tavus(sender, instance, created, **kwargs):
    if created:
        replica_id = instance.queue.replicId

        url = "https://tavusapi.com/v2/videos"
        payload = {
            "background_url": "",  # Puedes personalizar estos valores según sea necesario
            "replica_id": replica_id,      # Puedes personalizar estos valores según sea necesario
            "script": instance.videoText,
            "video_name": f"{instance.id}",
            "callback_url": f"http://{os.getenv('BACKEND_IP')}:8000/videos/tavus/callback/"
        }
        headers = {
            "x-api-key": os.getenv("TAVUS_KEY"),  # Reemplaza <api-key> con tu clave API real
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(response)
            instance.status = True
            instance.save()
        except requests.exceptions.RequestException as e:
            # Manejo de errores, puedes registrar el error o tomar alguna acción
            print(f"Error al crear el video en Tavus: {e}")