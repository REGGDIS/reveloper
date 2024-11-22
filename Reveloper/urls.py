from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import vista_evaluaciones, generar_informe_grafico_pdf, dashboard

urlpatterns = [
    path('home/', views.home, name='home'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('evaluaciones/', views.evaluaciones, name='evaluaciones'),
    path('tareas_por_desarrollar/', views.tareas_por_desarrollar,
         name='tareas_por_desarrollar'),
    path('print-template-dirs/', views.print_template_dirs,
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
    # Ajustar la ruta a 'dashboard/' directamente
    path('dashboard/', dashboard, name='dashboard'),
]
