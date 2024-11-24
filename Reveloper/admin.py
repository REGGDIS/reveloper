from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Proyecto, TareaPorDesarrollar, Evaluacion, TareasCompletadas, EvaluacionConfig
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('username', 'nombre', 'apellido', 'email',
                    'tareas_completadas')  # Añadido 'tareas_completadas'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


# Registro de Modelos
admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Proyecto)
admin.site.register(TareaPorDesarrollar)
admin.site.register(Evaluacion)
admin.site.register(EvaluacionConfig)


@admin.register(TareasCompletadas)
class TareasCompletadasAdmin(admin.ModelAdmin):
    list_display = ('tarea_original_id', 'titulo',
                    'estado', 'usuario', 'fecha_entrega')
