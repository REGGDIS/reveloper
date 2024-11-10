from django import forms
from .models import TareaPorDesarrollar


class TareaPorDesarrollarForm(forms.ModelForm):
    class Meta:
        model = TareaPorDesarrollar
        fields = ['titulo', 'descripcion',
                  'fecha_vencimiento', 'estado', 'proyecto']
