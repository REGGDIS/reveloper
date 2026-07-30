"""Configuración usada solo al ejecutar pruebas (SQLite en memoria)."""

import os

# Variables exclusivas de las pruebas automatizadas.
os.environ.setdefault(
    'DJANGO_SECRET_KEY',
    'dummy-test-secret-key-for-unit-testing-only-1234567890',
)
os.environ.setdefault('DJANGO_ENV', 'testing')
os.environ.setdefault('DJANGO_DEBUG', 'False')
os.environ.setdefault(
    'DJANGO_ALLOWED_HOSTS',
    'testserver,localhost,127.0.0.1',
)

from .settings import *  # noqa: E402,F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
