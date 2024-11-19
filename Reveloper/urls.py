from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import vista_evaluaciones, generar_informe_grafico_pdf


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
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('editar_tarea/<int:tarea_id>/',
         views.editar_tarea, name='editar_tarea'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate_task_pdf/', views.generate_task_pdf, name='generate_task_pdf'),
    path('generate_evaluation_pdf/', views.generate_evaluation_pdf,
         name='generate_evaluation_pdf'),
    path('generate_user_pdf/', views.generate_user_pdf, name='generate_user_pdf'),
    path('evaluaciones/', vista_evaluaciones, name='vista_evaluaciones'),
    path('generar_informe_grafico_pdf/', generar_informe_grafico_pdf,
         name='generar_informe_grafico_pdf'),
]
