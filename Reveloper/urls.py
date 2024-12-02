from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import vista_evaluaciones, generar_informe_grafico_pdf_desarrollador, generar_informe_grafico_pdf_admin, dashboard, buscar_proyectos, busqueda, buscar_tareas, generar_informe_pdf_busqueda, generar_informe_pdf_tareas, buscar_usuarios, generar_informe_pdf_usuarios

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
    path('generar_informe_grafico_pdf/', generar_informe_grafico_pdf_desarrollador,
         name='generar_informe_grafico_pdf'),
    path('generar_informe_grafico_pdf_admin/', generar_informe_grafico_pdf_admin,
         name='generar_informe_grafico_pdf_admin'),
    path('dashboard/', dashboard, name='dashboard'),

    # Nuevas rutas
    path('tareas/marcar_como_revision/<str:tarea_id>/',
         views.marcar_tarea_en_revision, name='marcar_tarea_en_revision'),
    path('revisar_tareas/', views.revisar_tareas, name='revisar_tareas'),
    path('buscar_proyectos/', buscar_proyectos, name='buscar_proyectos'),
    # Nueva ruta para buscar tareas
    path('buscar_tareas/', buscar_tareas, name='buscar_tareas'),
    # Nueva ruta para la sección de búsqueda
    path('busqueda/', busqueda, name='busqueda'),
    path('generar_informe_pdf_busqueda/', generar_informe_pdf_busqueda,
         # Nueva ruta para generar el informe PDF de búsqueda
         name='generar_informe_pdf_busqueda'),
    path('generar_informe_pdf_tareas/', generar_informe_pdf_tareas,
         name='generar_informe_pdf_tareas'),  # Nueva ruta para generar el informe PDF de tareas
    # Nueva ruta para buscar usuarios
    path('buscar_usuarios/', buscar_usuarios, name='buscar_usuarios'),
    path('generar_informe_pdf_usuarios/', generar_informe_pdf_usuarios,
         name='generar_informe_pdf_usuarios')  # Nueva ruta para generar el informe PDF de usuarios
]
