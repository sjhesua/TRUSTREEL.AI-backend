# company/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from videoManager.views import create_folder  # Asegúrate de que la ruta sea correcta
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_user_folder(sender, instance, created, **kwargs):
    if created:
        folder_name = instance.id
        create_folder(folder_name)