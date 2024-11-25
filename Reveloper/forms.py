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


class EvaluacionForm(forms.Form):
    tiempo_entrega = forms.DecimalField(
        max_digits=4, decimal_places=1, label="Tiempo de Entrega")
    complejidad_tarea = forms.DecimalField(
        max_digits=4, decimal_places=1, label="Complejidad de la Tarea")
    cumplimiento_requerimientos = forms.DecimalField(
        max_digits=4, decimal_places=1, label="Cumplimiento de Requerimientos")
    calidad_codigo = forms.DecimalField(
        max_digits=4, decimal_places=1, label="Calidad del Código")
