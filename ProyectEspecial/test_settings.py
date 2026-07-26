"""Configuración usada solo al ejecutar pruebas (SQLite en memoria)."""

import os

# Clave ficticia exclusiva únicamente para la ejecución de pruebas unitarias
os.environ.setdefault('DJANGO_SECRET_KEY', 'dummy-test-secret-key-for-unit-testing-only-1234567890')

from .settings import *  # noqa: F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
