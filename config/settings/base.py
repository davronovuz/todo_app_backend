import os
from pathlib import Path
from datetime import timedelta

# Loyiha asosiy papkasi
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Xavfsizlik kaliti (Productionda buni .env faylga olish SHART)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-halol-market-super-secret-key-2024')

# Debug rejimi (Productionda False bo'lishi kerak)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# -----------------------------------------------------------------------------
# Ilovalar (Apps)
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party Apps (Kutubxonalar)
    'rest_framework',  # API
    'rest_framework_simplejwt',  # JWT Auth
    'django_filters',  # Filterlash
    'corsheaders',  # CORS (Frontend uchun)
    'drf_yasg',  # Swagger Docs

    # Local Apps (Biz yozganlar)
    'apps.core',
    'apps.users',
    'apps.products',
    'apps.inventory',
    'apps.cart',
    'apps.orders',
    'apps.payments',
    'apps.reviews',
    'apps.wishlist',
    'apps.coupons',
    'apps.notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS eng yuqorida turishi kerak
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
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
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# -----------------------------------------------------------------------------
# Database (PostgreSQL)
# -----------------------------------------------------------------------------
# Hozircha SQLite (tezkor ishga tushirish uchun).
# .env fayl tayyor bo'lganda Postgresga o'tkazamiz.
import os
# ...
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_DATABASE', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('SQL_USER', ''),
        'PASSWORD': os.environ.get('SQL_PASSWORD', ''),
        'HOST': os.environ.get('SQL_HOST', ''),
        'PORT': os.environ.get('SQL_PORT', ''),
    }
}

# Agar Postgres ishlatmoqchi bo'lsangiz, buni kommentdan chiqaring:
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'halol_market_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
"""

# -----------------------------------------------------------------------------
# Auth & Password
# -----------------------------------------------------------------------------
AUTH_USER_MODEL = 'users.User'  # Bizning Custom User modelimiz

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------------------------------------------------------
# Internationalization (Til va Vaqt)
# -----------------------------------------------------------------------------
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# Static & Media
# -----------------------------------------------------------------------------
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------------------------------------------------------------
# REST Framework Config
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # Swagger uchun kerak
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Default holatda hamma joy yopiq
    ),
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.CustomPagination',  # O'zimiznikini ishlatamiz
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

# -----------------------------------------------------------------------------
# JWT Settings
# -----------------------------------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# -----------------------------------------------------------------------------
# CORS Headers (Frontend uchun)
# -----------------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True  # Developmentda True. Productionda aniq domainlar yoziladi.

# Default Primary Key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'