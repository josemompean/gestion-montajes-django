"""
Django settings for gestion_montajes project.
"""

from pathlib import Path
import os

# BASE_DIR: Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ Clave secreta (¡No la compartas en producción!)
SECRET_KEY = 'django-insecure-1&9d!16x6k=7gc#u3cf5clbba)9)_h0nr(#z$_u150$63q(!s3'

# ⚠️ Debug solo en desarrollo, nunca en producción
DEBUG = True  # Cambia a False en producción

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '127.0.0.1:59923']  # Dominios permitidos en producción

# URLs confiables para CSRF
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://127.0.0.1:59923']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'montajes',  # Asegúrate de que la app esté incluida aquí
]


# Middlewares de Django
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs
ROOT_URLCONF = 'gestion_montajes.urls'

# Configuración de Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Cambia esto a lista vacía
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'gestion_montajes.wsgi.application'

# Configuración de la Base de Datos (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Proyectogestion_montajes',
        'USER': 'root',
        'PASSWORD': '0000',  # Asegúrate de usar la contraseña correcta
        'HOST': '127.0.0.1',  # O 'localhost'
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',  # Soporte para caracteres especiales
        },
    }
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración de idioma y zona horaria
LANGUAGE_CODE = 'es'
TIME_ZONE = 'Europe/Madrid'  # Ajusta según tu país
USE_I18N = True
USE_TZ = False  # Desactivamos el soporte de zonas horarias para evitar problemas con MySQL
# Archivos estáticos (CSS, JS, imágenes)
# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'  

# Asegúrate de que esta línea está presente
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirección de login y logout
LOGIN_REDIRECT_URL = '/montajes/'  # A dónde redirigir después del login
LOGOUT_REDIRECT_URL = '/login/'  # A dónde redirigir después del logout
LOGIN_URL = '/login/'  # URL de login si un usuario no autenticado intenta acceder

# Add or update this setting
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Seguridad en Producción
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
