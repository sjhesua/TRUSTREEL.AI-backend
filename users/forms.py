# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from company.models import Company  # Importa el modelo Company

class CustomUserCreationForm(UserCreationForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), required=False)  # Opcional

    class Meta:
        model = User
        fields = ('username', 'email', 'company', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), required=False)  # Opcional

    class Meta:
        model = User
        fields = ('username', 'email', 'company')
