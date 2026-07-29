from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import (
    Evaluacion,
    EvaluacionConfig,
    Proyecto,
    TareaPorDesarrollar,
    TareasCompletadas,
    Usuario,
)


@admin.register(Usuario)
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = (
        'username',
        'nombre',
        'apellido',
        'email',
        'is_active',
        'tareas_completadas',
    )
    search_fields = (
        'username',
        'nombre',
        'apellido',
        'email',
    )
    ordering = ('username',)

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'password',
                ),
            },
        ),
        (
            'Información personal',
            {
                'fields': (
                    'nombre',
                    'apellido',
                    'email',
                ),
            },
        ),
        (
            'Permisos',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            'Fechas importantes',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                ),
            },
        ),
        (
            'Desempeño',
            {
                'fields': (
                    'tareas_completadas',
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'nombre',
                    'apellido',
                    'password1',
                    'password2',
                ),
            },
        ),
    )


admin.site.register(Proyecto)
admin.site.register(TareaPorDesarrollar)
admin.site.register(Evaluacion)
admin.site.register(EvaluacionConfig)


@admin.register(TareasCompletadas)
class TareasCompletadasAdmin(admin.ModelAdmin):
    list_display = (
        'tarea_original_id',
        'titulo',
        'estado',
        'usuario',
        'fecha_entrega',
    )
