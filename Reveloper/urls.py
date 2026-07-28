from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('evaluaciones/', views.evaluaciones, name='evaluaciones'),
    path(
        'tareas_por_desarrollar/',
        views.tareas_por_desarrollar,
        name='tareas_por_desarrollar',
    ),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path(
        'editar_tarea/<str:tarea_id>/',
        views.editar_tarea,
        name='editar_tarea',
    ),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path(
        'generate_task_pdf/',
        views.generate_task_pdf,
        name='generate_task_pdf',
    ),
    path(
        'generate_evaluation_pdf/',
        views.generate_evaluation_pdf,
        name='generate_evaluation_pdf',
    ),
    path(
        'generate_user_pdf/',
        views.generate_user_pdf,
        name='generate_user_pdf',
    ),
    path(
        'generar_informe_grafico_pdf/',
        views.generar_informe_grafico_pdf_desarrollador,
        name='generar_informe_grafico_pdf',
    ),
    path(
        'generar_informe_grafico_pdf_admin/',
        views.generar_informe_grafico_pdf_admin,
        name='generar_informe_grafico_pdf_admin',
    ),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'tareas/marcar_como_revision/<str:tarea_id>/',
        views.marcar_tarea_en_revision,
        name='marcar_tarea_en_revision',
    ),
    path(
        'revisar_tareas/',
        views.revisar_tareas,
        name='revisar_tareas',
    ),
    path(
        'buscar_proyectos/',
        views.buscar_proyectos,
        name='buscar_proyectos',
    ),
    path(
        'buscar_tareas/',
        views.buscar_tareas,
        name='buscar_tareas',
    ),
    path('busqueda/', views.busqueda, name='busqueda'),
    path(
        'generar_informe_pdf_busqueda/',
        views.generar_informe_pdf_busqueda,
        name='generar_informe_pdf_busqueda',
    ),
    path(
        'generar_informe_pdf_tareas/',
        views.generar_informe_pdf_tareas,
        name='generar_informe_pdf_tareas',
    ),
    path(
        'buscar_usuarios/',
        views.buscar_usuarios,
        name='buscar_usuarios',
    ),
    path(
        'generar_informe_pdf_usuarios/',
        views.generar_informe_pdf_usuarios,
        name='generar_informe_pdf_usuarios',
    ),
    path(
        'exportar_tareas_excel/',
        views.exportar_tareas_excel,
        name='exportar_tareas_excel',
    ),
    path(
        'exportar_proyectos_excel/',
        views.exportar_proyectos_excel,
        name='exportar_proyectos_excel',
    ),
    path(
        'exportar_usuarios_excel/',
        views.exportar_usuarios_excel,
        name='exportar_usuarios_excel',
    ),
    path(
        'exportar_todos_usuarios_excel/',
        views.exportar_todos_usuarios_excel,
        name='exportar_todos_usuarios_excel',
    ),
    path(
        'exportar_todos_proyectos_excel/',
        views.exportar_todos_proyectos_excel,
        name='exportar_todos_proyectos_excel',
    ),
    path(
        'exportar_todas_tareas_excel/',
        views.exportar_todas_tareas_excel,
        name='exportar_todas_tareas_excel',
    ),
    path(
        'exportar_todas_evaluaciones_excel/',
        views.exportar_todas_evaluaciones_excel,
        name='exportar_todas_evaluaciones_excel',
    ),
]