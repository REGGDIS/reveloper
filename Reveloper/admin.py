from django.contrib import admin
from .models import Usuario, Proyecto, TareaPorDesarrollar, TareaDesarrollada, Evaluacion

# Registro de Modelos
admin.site.register(Usuario)
admin.site.register(Proyecto)
admin.site.register(TareaPorDesarrollar)
admin.site.register(TareaDesarrollada)
admin.site.register(Evaluacion)
