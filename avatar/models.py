from django.db import models
from django.core.exceptions import ValidationError

def validate_image(image):
    file_size = image.file.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f'El tamaño máximo permitido es de {limit_mb}MB')

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='images/replica/', validators=[validate_image])
    code = models.CharField(max_length=100)
    replicaName = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    style = models.CharField(max_length=1000, default='')