from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Proyecto, TareaPorDesarrollar, Usuario, Evaluacion
from .forms import TareaPorDesarrollarForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.units import inch
import io


# Función de Verificación para Administradores
def es_admin(user):
    return user.is_superuser

# Vista para el inicio de sesión personalizado


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('/reveloper/home/')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

# Vista protegida para el home, accesible solo para usuarios autenticados


@login_required
def home(request):
    context = {
        'usuario': request.user
    }
    return render(request, 'home.html', context)

# Vista para imprimir las carpetas de plantillas configuradas


def print_template_dirs(request):
    print(settings.TEMPLATES[0]['DIRS'])
    return HttpResponse('Template Dirs Printed')

# Vista para la página de usuarios, accesible solo para usuarios autenticados


@login_required
@user_passes_test(es_admin)
def usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})

# Vista para la página de proyectos, accesible solo para usuarios autenticados


@login_required
def proyectos(request):
    proyectos = Proyecto.objects.all()
    for proyecto in proyectos:
        proyecto.tareas = TareaPorDesarrollar.objects.filter(proyecto=proyecto)

    # Definir context fuera del bucle for
    context = {
        'proyectos': proyectos
    }

    return render(request, 'proyectos.html', context)

# Vista para la página de evaluaciones, accesible solo para usuarios autenticados


@login_required
def evaluaciones(request):
    if request.user.is_superuser:  # El administrador puede ver todas las evaluaciones
        evaluaciones = Evaluacion.objects.all()
    else:  # Otros usuarios solo ven sus evaluaciones
        evaluaciones = Evaluacion.objects.filter(usuario=request.user)

    return render(request, 'evaluaciones.html', {'evaluaciones': evaluaciones})

# Vista para la página de tareas por desarrollar, accesible solo para usuarios autenticados


@login_required
def tareas_por_desarrollar(request):
    if request.user.is_superuser:
        # Si es administrador, mostrar todas las tareas
        tareas = TareaPorDesarrollar.objects.select_related(
            'proyecto', 'usuario').all()
    else:
        # Si no es administrador, mostrar solo las tareas asignadas al usuario
        tareas = TareaPorDesarrollar.objects.select_related(
            'proyecto', 'usuario').filter(usuario=request.user)
    return render(request, 'tareas.html', {'tareas': tareas})


@login_required
@user_passes_test(es_admin)
def crear_tarea(request):
    if request.method == 'POST':
        form = TareaPorDesarrollarForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = request.user  # Asignar el usuario autenticado
            tarea.save()  # Guardar la tarea con el usuario asignado
            return redirect('proyectos')
    else:
        form = TareaPorDesarrollarForm()
    return render(request, 'crear_tarea.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(TareaPorDesarrollar, pk=tarea_id)
    if request.method == 'POST':
        form = TareaPorDesarrollarForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            # Redirige a la lista de proyectos o donde prefieras
            return redirect('proyectos')
        else:
            form = TareaPorDesarrollarForm(instance=tarea)
        return render(request, 'editar_tarea.html', {'form': form})


@login_required
def generate_pdf(request):
    # Crear un buffer de bytes para el PDF
    buffer = io.BytesIO()
    # Crear el PDF
    p = canvas.Canvas(buffer, pagesize=letter)

    # Registrar y usar una fuente personalizada
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    p.setFont("Arial", 12)

    # Añadir una imagen de logotipo en la parte superior del documento
    p.drawImage("Reveloper/static/img/logos/logo-reveloper.png",
                100, 700, width=2*inch, height=1*inch)

    # Título del documento
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.darkblue)
    p.drawString(100, 650, "Informe de Proyecto")

    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(100, 630, f"Usuario: {request.user.username}")
    p.drawString(100, 615, "Lista de Proyectos:")

    # Margen inferior para el contenido
    bottom_margin = 50

    # Obtener datos del contexto
    projects = Proyecto.objects.all()
    y = 595
    for project in projects:
        if y < bottom_margin:  # Salto de página si el espacio es insuficiente
            p.showPage()
            y = 750
            p.setFont("Helvetica", 12)

        p.drawString(100, y, f"ID: {project.id}, Nombre: {project.nombre}")
        y -= 15
        p.drawString(100, y, f"Descripción: {project.descripcion}")
        y -= 15
        p.drawString(100, y, f"Fecha de Inicio: {project.fecha_inicio}")
        y -= 15
        p.drawString(100, y, f"Fecha de Fin: {project.fecha_fin}")
        y -= 15
        p.drawString(100, y, f"Estado: {project.get_estado_display()}")
        y -= 15
        y -= 10  # Añadir un pequeño espacio antes de las tareas

        # Añadir tareas al PDF
        tareas = TareaPorDesarrollar.objects.filter(
            proyecto=project).select_related('usuario')
        for tarea in tareas:
            if y < bottom_margin:  # Salto de página si el espacio es insuficiente
                p.showPage()
                y = 750
                p.setFont("Helvetica", 12)

            p.drawString(120, y, f"Tarea: {tarea.titulo}")
            y -= 15
            p.drawString(120, y, f"Asignado a: {tarea.usuario.first_name} {
                         tarea.usuario.last_name}")
            y -= 15
            p.drawString(120, y, f"Estado: {tarea.estado}")
            y -= 15
            p.drawString(120, y, f"Fecha de Creación: {tarea.fecha_creacion}")
            y -= 15
            p.drawString(120, y, f"Fecha de Vencimiento: {
                         tarea.fecha_vencimiento}")
            y -= 15
            y -= 5  # Añadir un pequeño espacio entre tareas

        y -= 10  # Añadir un pequeño espacio antes de la línea
        p.setStrokeColor(colors.grey)
        # Añadir una línea horizontal más corta para separar proyectos
        p.line(100, y, 500, y)
        y -= 20  # Añadir un espacio adicional entre proyectos

        # Verificar si el último contenido está demasiado cerca del borde
        if y < bottom_margin:
            p.showPage()
            y = 750
            p.setFont("Helvetica", 12)

    # Cerrar y guardar el PDF
    p.showPage()
    p.save()

    # Obtener el valor de los bytes del buffer y escribirlo en la respuesta
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


def generate_task_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Registrar y usar una fuente personalizada
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    p.setFont("Arial", 12)

    # Añadir una imagen de logotipo en la parte superior del documento
    p.drawImage("Reveloper/static/img/logos/logo-reveloper.png",
                100, 700, width=2*inch, height=1*inch)

    # Título del documento
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.darkblue)
    p.drawString(100, 650, "Informe de Tareas")

    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(100, 630, f"Usuario: {request.user.username}")

    # Verificar si el usuario es administrador
    if request.user.is_superuser:
        tareas = TareaPorDesarrollar.objects.all()
        p.drawString(100, 610, "Lista de Todas las Tareas:")
    else:
        tareas = TareaPorDesarrollar.objects.filter(usuario=request.user)
        p.drawString(100, 610, "Lista de Tareas Asignadas:")

    y = 590
    for tarea in tareas:
        p.drawString(100, y, f"Título: {tarea.titulo}")
        y -= 15
        p.drawString(100, y, f"Descripción: {tarea.descripcion}")
        y -= 15
        p.drawString(100, y, f"Estado: {tarea.estado}")
        y -= 15
        p.drawString(100, y, f"Fecha de Creación: {tarea.fecha_creacion}")
        y -= 15
        p.drawString(100, y, f"Fecha de Vencimiento: {
                     tarea.fecha_vencimiento}")
        y -= 15
        p.drawString(100, y, f"Proyecto: {tarea.proyecto.nombre}")
        y -= 15
        p.drawString(100, y, f"Asignado a: {tarea.usuario.first_name} {
                     tarea.usuario.last_name}")
        y -= 30

        # Ajustar posición de la línea divisoria
        p.setStrokeColor(colors.grey)
        line_y = y + 7.5  # Centrar la línea divisoria entre tareas
        p.line(100, line_y, 500, line_y)
        y -= 10  # Añadir un pequeño margen después de la línea

    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


def generate_evaluation_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Registrar y usar una fuente personalizada
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    p.setFont("Arial", 12)

    # Añadir una imagen de logotipo en la parte superior del documento
    p.drawImage("Reveloper/static/img/logos/logo-reveloper.png",
                100, 700, width=2*inch, height=1*inch)

    # Título del documento
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.darkblue)
    p.drawString(100, 650, "Informe de Evaluaciones")

    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(100, 630, f"Usuario: {request.user.username}")

    # Verificar si el usuario es administrador
    if request.user.is_superuser:
        evaluaciones = Evaluacion.objects.all()
        p.drawString(100, 610, "Lista de Todas las Evaluaciones:")
    else:
        evaluaciones = Evaluacion.objects.filter(usuario=request.user)
        p.drawString(100, 610, "Lista de Evaluaciones Asignadas:")

    y = 590
    for evaluacion in evaluaciones:
        p.drawString(100, y, f"Título: {evaluacion.titulo}")
        y -= 15
        p.drawString(100, y, f"Calificación: {evaluacion.calificacion}")
        y -= 15
        if evaluacion.tarea:
            p.drawString(100, y, f"Tarea: {evaluacion.tarea.titulo}")
        else:
            p.drawString(100, y, "Tarea: Sin Tarea Asignada")
        y -= 15
        p.drawString(100, y, f"Asignado a: {evaluacion.usuario.first_name} {
                     evaluacion.usuario.last_name}")
        y -= 15
        p.drawString(100, y, f"Fecha de Evaluación: {
                     evaluacion.fecha_evaluacion}")
        y -= 15
        p.drawString(100, y, f"Proyecto: {evaluacion.proyecto.nombre}")
        y -= 30

        # Ajustar posición de la línea divisoria
        p.setStrokeColor(colors.grey)
        line_y = y + 7.5  # Centrar la línea divisoria entre evaluaciones
        p.line(100, line_y, 500, line_y)
        y -= 10  # Añadir un pequeño margen después de la línea

    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


def generate_user_pdf(request):
    # Esta vista sólo debe ser accesible para administradores
    if not request.user.is_superuser:
        return HttpResponse("No tienes permiso para acceder a esta página.", status=403)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Registrar y usar una fuente personalizada
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    p.setFont("Arial", 12)

    # Añadir una imagen de logotipo en la parte superior del documento
    p.drawImage("Reveloper/static/img/logos/logo-reveloper.png",
                100, 700, width=2*inch, height=1*inch)

    # Título del documento
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.darkblue)
    p.drawString(100, 650, "Informe de Usuarios")

    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(100, 630, f"Generado por: {request.user.username}")
    p.drawString(100, 615, "Lista de Usuarios:")

    usuarios = Usuario.objects.all()
    y = 595
    for usuario in usuarios:
        p.drawString(100, y, f"Nombre: {usuario.first_name} {
                     usuario.last_name}")
        y -= 15
        p.drawString(100, y, f"Email: {usuario.email}")
        y -= 15
        p.drawString(100, y, f"Fecha de Registro: {usuario.date_joined}")
        y -= 30

        # Ajustar posición de la línea divisoria
        p.setStrokeColor(colors.grey)
        line_y = y + 7.5  # Centrar la línea divisoria entre usuarios
        p.line(100, line_y, 500, line_y)
        y -= 10  # Añadir un pequeño margen después de la línea

    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
