import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'your-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'turismo_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mi_examen.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

WSGI_APPLICATION = 'mi_examen.wsgi.application'

DB_ENGINE = os.getenv("DB_ENGINE", "postgresql")

if DB_ENGINE == "postgresql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('PG_NAME'),
            'USER': os.getenv('PG_USER'),
            'PASSWORD': os.getenv('PG_PASSWORD'),
            'HOST': os.getenv('PG_HOST'),
            'PORT': os.getenv('PG_PORT'),
        }
    }
elif DB_ENGINE == "oracle":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.oracle',
            'NAME': os.getenv('ORACLE_NAME'),
            'USER': os.getenv('ORACLE_USER'),
            'PASSWORD': os.getenv('ORACLE_PASSWORD'),
            'HOST': os.getenv('ORACLE_HOST'),
            'PORT': os.getenv('ORACLE_PORT'),
        }
    }

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
