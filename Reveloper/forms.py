from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import TareaPorDesarrollar, Usuario


class TareaPorDesarrollarForm(forms.ModelForm):
    class Meta:
        model = TareaPorDesarrollar
        fields = ['titulo', 'descripcion',
                  'fecha_vencimiento', 'estado', 'proyecto']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = '__all__'
