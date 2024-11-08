from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  # Ruta para la página de inicio
    path('print-template-dirs/', views.print_template_dirs,
         name='print_template_dirs'),  # Ruta para verificar plantillas (temporal)
]
