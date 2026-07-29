import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url

# ── Base directory ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ── Inject ImageKit keys into os.environ before any app is imported ────────────
# imagekitio reads from os.environ at module import time, so these must be set
# before Django's app registry loads anything.
os.environ['IMAGEKIT_PRIVATE_KEY']  = config('IMAGEKIT_PRIVATE_KEY')
os.environ['IMAGEKIT_PUBLIC_KEY']   = config('IMAGEKIT_PUBLIC_KEY')
os.environ['IMAGEKIT_URL_ENDPOINT'] = config('IMAGEKIT_URL_ENDPOINT')

# ── Security ───────────────────────────────────────────────────────────────────
SECRET_KEY    = config('SECRET_KEY')
DEBUG         = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())
SITE_URL      = config('SITE_URL', default='https://fertileus.com.ng').rstrip('/')
INDEXNOW_KEY  = config('INDEXNOW_KEY', default='')

# ── Force custom error pages even in DEBUG mode ───────────────────────────────
FORCE_CUSTOM_ERROR_PAGES = config('FORCE_CUSTOM_ERROR_PAGES', default=False, cast=bool)

# ── Maintenance Mode ───────────────────────────────────────────────────────────
MAINTENANCE_MODE = config('MAINTENANCE_MODE', default=False, cast=bool)

# ── Google Indexing API ───────────────────────────────────────────────────────────
GOOGLE_SERVICE_ACCOUNT_JSON = config('GOOGLE_SERVICE_ACCOUNT_JSON', default='')

# ── Installed apps ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'Home',
    'aibot',
]

SITE_ID = 1

# ── Middleware ─────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'Home.middleware.MaintenanceModeMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FertileUs.urls'

# ── Templates ──────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Home.context_processors.seo',
            ],
        },
    },
]

WSGI_APPLICATION = 'FertileUs.wsgi.application'

# ── Database ───────────────────────────────────────────────────────────────────
DATABASES = {
    'default': dj_database_url.parse(
        config('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ── Password validation ────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalisation ───────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Africa/Lagos'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

# ── Static files ──────────────────────────────────────────────────────────────
STATIC_URL       = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT      = BASE_DIR / 'staticfiles'

# ── File storage ──────────────────────────────────────────────────────────────
# Uses the custom ImageKitStorage backend in Home/storage.py
# Uploads go to ImageKit CDN; the full CDN URL is stored in the DB field.
STORAGES = {
    'default': {
        'BACKEND': 'Home.storage.ImageKitStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# MEDIA_URL is the ImageKit base URL — used as fallback in storage.url()
MEDIA_URL = config('IMAGEKIT_URL_ENDPOINT') + '/'

# ── ImageKit credentials ───────────────────────────────────────────────────────
IMAGEKIT_STORAGE = {
    'PRIVATE_KEY':  config('IMAGEKIT_PRIVATE_KEY'),
    'PUBLIC_KEY':   config('IMAGEKIT_PUBLIC_KEY'),
    'URL_ENDPOINT': config('IMAGEKIT_URL_ENDPOINT'),
    'UPLOAD_OPTIONS': {
        'use_unique_file_name': True,
        'folder':               '/fertileus/',
        'is_private_file':      False,
        'overwrite_file':       True,
    },
}

# ── Default primary key ────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
