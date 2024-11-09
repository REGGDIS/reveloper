from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  # Ruta para la página de inicio
    # Ruta para la página de usuarios
    path('usuarios/', views.usuarios, name='usuarios'),
    # Ruta para la lista de proyectos
    path('proyectos/', views.proyectos, name='proyectos'),
    # Ruta para la página de evaluaciones
    path('evaluaciones/', views.evaluaciones, name='evaluaciones'),
    path('tareas_por_desarrollar/', views.tareas_por_desarrollar,
         name='tareas_por_desarrollar'),  # Ruta para la página de tareas por desarrollar
    path('print-template-dirs/', views.print_template_dirs,
         # Ruta para verificar plantillas (temporal)
         name='print_template_dirs'),
]
