from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .models import Proyecto, TareaPorDesarrollar, Usuario
from .forms import TareaPorDesarrollarForm


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
def usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})

# Vista para la página de proyectos, accesible solo para usuarios autenticados


@login_required
def proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos.html', {'proyectos': proyectos})

# Vista para la página de evaluaciones, accesible solo para usuarios autenticados


@login_required
def evaluaciones(request):
    return render(request, 'evaluaciones.html')

# Vista para la página de tareas por desarrollar, accesible solo para usuarios autenticados


@login_required
def tareas_por_desarrollar(request):
    tareas = TareaPorDesarrollar.objects.all()
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
            # Redirige a la lista de proyectos o donde prefieras
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
