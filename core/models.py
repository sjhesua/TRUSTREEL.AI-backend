from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    subdominio = models.CharField(max_length=100, unique=True)
    # Otros campos relevantes