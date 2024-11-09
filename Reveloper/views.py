from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .models import Proyecto, TareaPorDesarrollar, Usuario

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
