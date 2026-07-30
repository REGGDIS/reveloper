import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv


# Rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde .env en la raíz del proyecto
load_dotenv(BASE_DIR / '.env')


# Utilidades para variables de entorno
TRUE_VALUES = ('true', '1', 't', 'yes')


def _env_bool(name, default=False):
    value = os.getenv(name, str(default))
    return value.strip().lower() in TRUE_VALUES


def _env_list(name):
    raw_value = os.getenv(name, '')
    return [
        value.strip()
        for value in raw_value.split(',')
        if value.strip()
    ]


# Entorno de ejecución
ENVIRONMENT = os.getenv(
    'DJANGO_ENV',
    'development',
).strip().lower()

IS_PRODUCTION = ENVIRONMENT == 'production'


# Configuración principal de seguridad
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

if not SECRET_KEY:
    raise ImproperlyConfigured(
        'La variable de entorno DJANGO_SECRET_KEY '
        'no está configurada.'
    )

DEBUG = _env_bool('DJANGO_DEBUG', False)

ALLOWED_HOSTS = _env_list('DJANGO_ALLOWED_HOSTS')

CSRF_TRUSTED_ORIGINS = _env_list(
    'DJANGO_CSRF_TRUSTED_ORIGINS'
)


# Validaciones obligatorias para producción
if IS_PRODUCTION:
    if DEBUG:
        raise ImproperlyConfigured(
            'DJANGO_DEBUG debe ser False en producción.'
        )

    if not ALLOWED_HOSTS:
        raise ImproperlyConfigured(
            'DJANGO_ALLOWED_HOSTS debe contener al menos '
            'un dominio en producción.'
        )

    if (
        len(SECRET_KEY) < 50
        or SECRET_KEY.startswith('django-insecure-')
    ):
        raise ImproperlyConfigured(
            'DJANGO_SECRET_KEY debe ser una clave segura '
            'de al menos 50 caracteres en producción.'
        )


# Aplicaciones instaladas
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Reveloper',
]

AUTH_USER_MODEL = 'Reveloper.Usuario'


# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Seguridad HTTP
SECURE_SSL_REDIRECT = IS_PRODUCTION
SESSION_COOKIE_SECURE = IS_PRODUCTION
CSRF_COOKIE_SECURE = IS_PRODUCTION

SECURE_HSTS_SECONDS = (
    int(
        os.getenv(
            'DJANGO_SECURE_HSTS_SECONDS',
            '3600',
        )
    )
    if IS_PRODUCTION
    else 0
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    IS_PRODUCTION
    and _env_bool(
        'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS',
        False,
    )
)

SECURE_HSTS_PRELOAD = (
    IS_PRODUCTION
    and _env_bool(
        'DJANGO_SECURE_HSTS_PRELOAD',
        False,
    )
)

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'

SESSION_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = 'DENY'


# Configuración opcional para proxy inverso
if _env_bool('DJANGO_USE_X_FORWARDED_PROTO', False):
    SECURE_PROXY_SSL_HEADER = (
        'HTTP_X_FORWARDED_PROTO',
        'https',
    )


# Configuración de URLs y plantillas
ROOT_URLCONF = 'ProyectEspecial.urls'

TEMPLATES = [
    {
        'BACKEND': (
            'django.template.backends.django.'
            'DjangoTemplates'
        ),
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'Reveloper' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                (
                    'django.template.context_processors.'
                    'debug'
                ),
                (
                    'django.template.context_processors.'
                    'request'
                ),
                (
                    'django.contrib.auth.context_processors.'
                    'auth'
                ),
                (
                    'django.contrib.messages.'
                    'context_processors.messages'
                ),
            ],
        },
    },
]

WSGI_APPLICATION = 'ProyectEspecial.wsgi.application'


# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'reveloper'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': (
                "SET sql_mode='STRICT_TRANS_TABLES'"
            ),
        },
    }
}


# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]


# Internacionalización
LANGUAGE_CODE = 'es-us'

TIME_ZONE = 'America/Santiago'

USE_I18N = True
USE_TZ = True


# Archivos estáticos
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'Reveloper' / 'static',
]


# Campo de clave primaria predeterminado
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Redirecciones de autenticación
LOGIN_REDIRECT_URL = '/reveloper/home/'
LOGOUT_REDIRECT_URL = '/login/'


# Configuración de Jazzmin
JAZZMIN_SETTINGS = {
    'login_logo': 'img/logos/logo-reveloper.png',
    'custom_css': 'css/custom_admin.css',
    'welcome_sign': 'Login Admin Reveloper',
    'site_logo': 'img/logos/logo-reveloper.png',
}
