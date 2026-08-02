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


@admin.register(EvaluacionConfig)
class EvaluacionConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if EvaluacionConfig.objects.exists():
            return False

        return super().has_add_permission(request)


@admin.register(TareasCompletadas)
class TareasCompletadasAdmin(admin.ModelAdmin):
    list_display = (
        'tarea_original_id',
        'titulo',
        'estado',
        'usuario',
        'fecha_entrega',
    )
