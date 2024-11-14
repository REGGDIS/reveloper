from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Proyecto, TareaPorDesarrollar, TareaDesarrollada, Evaluacion
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
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
admin.site.register(TareaDesarrollada)
admin.site.register(Evaluacion)
