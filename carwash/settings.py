from pathlib import Path
import os

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.environ.get(name, 'true' if default else 'false').lower() in ('1', 'true', 'yes', 'on')


def env_list(name, default):
    return [item.strip() for item in os.environ.get(name, default).split(',') if item.strip()]


# SECURITY WARNING: keep the secret key secret in production!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = env_bool('DJANGO_DEBUG', default=True)

if SECRET_KEY:
    pass
elif DEBUG:
    SECRET_KEY = 'django-insecure-dev-only-key-do-not-use-in-production'
else:
    raise ImproperlyConfigured('DJANGO_SECRET_KEY must be set when DEBUG is disabled.')

ALLOWED_HOSTS = env_list(
    'DJANGO_ALLOWED_HOSTS',
    'localhost,127.0.0.1,car-washui2.onrender.com,carwash-z66a.onrender.com',
)

CSRF_TRUSTED_ORIGINS = env_list(
    'DJANGO_CSRF_TRUSTED_ORIGINS',
    'https://car-washui2.onrender.com,https://carwash-z66a.onrender.com',
)

# Render terminates TLS; trust its forwarded proto header.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# HTTPS / security hardening (only enforced outside DEBUG).
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'bookings',
    'services',
    'dashboard',
    'api',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'carwash.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'carwash.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Tunis'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Serve static via WhiteNoise with brotli/gzip compression.
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

WHITENOISE_MAX_AGE = 60 * 60 * 24

# Serve straight from STATICFILES_DIRS (committed static/) so production works
# even if collectstatic is not run by the build step. On-the-fly compression
# still applies. Set to False once the deploy pipeline collects static.
WHITENOISE_USE_FINDERS = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/connexion/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email — Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('SMTP_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')
