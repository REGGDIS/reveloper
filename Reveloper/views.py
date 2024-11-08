from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse

# Creación de vistas


@login_required
def home(request):
    return render(request, 'home.html')


def print_template_dirs(request):
    print(settings.TEMPLATES[0]['DIRS'])
    return HttpResponse('Template Dirs Printed')
