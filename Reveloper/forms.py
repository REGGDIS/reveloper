from decimal import Decimal
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import TareaPorDesarrollar, Usuario


class TareaPorDesarrollarForm(forms.ModelForm):
    class Meta:
        model = TareaPorDesarrollar
        fields = [
            'titulo',
            'descripcion',
            'fecha_vencimiento',
            'estado',
            'proyecto',
            'usuario',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['usuario'].queryset = Usuario.objects.filter(
            is_active=True,
            is_superuser=False,
            is_staff=False,
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = (
            'username',
            'email',
            'nombre',
            'apellido',
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = '__all__'


class EvaluacionForm(forms.Form):
    CRITERIOS = (
        'tiempo_entrega',
        'complejidad_tarea',
        'cumplimiento_requerimientos',
        'calidad_codigo',
    )

    tiempo_entrega = forms.DecimalField(
        max_digits=4,
        decimal_places=1,
        label='Tiempo de Entrega',
    )
    complejidad_tarea = forms.DecimalField(
        max_digits=4,
        decimal_places=1,
        label='Complejidad de la Tarea',
    )
    cumplimiento_requerimientos = forms.DecimalField(
        max_digits=4,
        decimal_places=1,
        label='Cumplimiento de Requerimientos',
    )
    calidad_codigo = forms.DecimalField(
        max_digits=4,
        decimal_places=1,
        label='Calidad del Código',
    )

    def __init__(self, *args, evaluacion_config=None, **kwargs):
        super().__init__(*args, **kwargs)

        limites = {
            'tiempo_entrega': Decimal('25.0'),
            'complejidad_tarea': Decimal('25.0'),
            'cumplimiento_requerimientos': Decimal('25.0'),
            'calidad_codigo': Decimal('25.0'),
        }

        if evaluacion_config is not None:
            limites = {
                criterio: getattr(evaluacion_config, criterio)
                for criterio in self.CRITERIOS
            }
            self.nota_maxima = Decimal(
                str(evaluacion_config.nota_maxima)
            )
        else:
            self.nota_maxima = Decimal('100.0')

        for criterio, maximo in limites.items():
            field = self.fields[criterio]

            field.validators.extend(
                [
                    MinValueValidator(Decimal('0.0')),
                    MaxValueValidator(maximo),
                ]
            )

            field.widget.attrs.update(
                {
                    'min': '0',
                    'max': str(maximo),
                    'step': '0.1',
                }
            )

    def clean(self):
        cleaned_data = super().clean()

        if any(
            cleaned_data.get(criterio) is None
            for criterio in self.CRITERIOS
        ):
            return cleaned_data

        total = sum(
            cleaned_data[criterio]
            for criterio in self.CRITERIOS
        )

        if total > self.nota_maxima:
            raise forms.ValidationError(
                (
                    'La calificación total no puede superar '
                    f'{self.nota_maxima}.'
                )
            )

        return cleaned_data
