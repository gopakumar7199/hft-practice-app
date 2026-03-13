import os
import json
import boto3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Secret Key ───────────────────────────────────────────────────────────────
# In production: fetched from AWS Secrets Manager
# In local dev:  uses environment variable or fallback
SECRET_KEY = os.environ.get('SECRET_KEY', 'local-dev-secret-key-change-in-production')

# ─── Environment ──────────────────────────────────────────────────────────────
ENVIRONMENT = os.environ.get('ENVIRONMENT_TYPE', 'local')
DEBUG = ENVIRONMENT in ['local', 'practice']

ALLOWED_HOSTS = ['*']  # Tightened in production via ALB/CloudFront

# ─── Applications ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'apps.health',
    'apps.trades',
    'apps.users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_gateway.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'api_gateway.wsgi.application'

# ─── Database ─────────────────────────────────────────────────────────────────
# DATABASE_URL injected from AWS Secrets Manager via ECS task definition
DATABASE_URL = os.environ.get('DATABASE_URL', '')

if DATABASE_URL:
    # Parse postgresql://user:pass@host:port/dbname
    import urllib.parse
    parsed = urllib.parse.urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed.path[1:],
            'USER': parsed.username,
            'PASSWORD': parsed.password,
            'HOST': parsed.hostname,
            'PORT': parsed.port or 5432,
            'OPTIONS': {'connect_timeout': 10},
        }
    }
else:
    # Local development fallback — SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ─── Celery / Redis ───────────────────────────────────────────────────────────
# CELERY_BROKER_URL injected from ECS environment variables
# Points to shared ElastiCache Redis cluster
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# ─── Static Files ─────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ─── CORS ─────────────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [] if DEBUG else [
    'https://your-cloudfront-domain.cloudfront.net',
]

# ─── REST Framework ───────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# ─── Logging ──────────────────────────────────────────────────────────────────
# ECS Fargate captures stdout automatically and ships to CloudWatch Logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
