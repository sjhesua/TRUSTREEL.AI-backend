# admin.py

from django.contrib import admin
from .models import Company,Profile,CustomUser

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subdomain')  # Asegúrate de que estos campos existen en tu modelo
    search_fields = ('name',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'verified')  # Asegúrate de que estos campos existen en tu modelo
    search_fields = ('user__username',)
    list_editable = ['verified']

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'company')  # Asegúrate de que estos campos existen en tu modelo
    search_fields = ('username', 'company__name')

# Registrar el modelo Company con la clase de administrador personalizada
admin.site.register(Company, CompanyAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomUser, UserAdmin)