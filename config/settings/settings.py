import os
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
try:
    owner = __file__.split('/')[2].lower()
except:
    owner = __file__.split('\\')[2].lower()

devs = ['emizy']
if owner in devs:
    WHICH = 'dev_settings'
else:
    WHICH = 'prod_settings'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core',
    'apps.finance',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
DATETIME_FORMAT = '%d/%m/%Y %I:%M %p'
TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True
AUTH_USER_MODEL = 'core.User'
AUTHENTICATION_BACKENDS = (
    'apps.utils.authentication.CustomAuthBackend',
)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "../static")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../media')
# AUTH_USER_MODEL = 'core.User'
# AUTHENTICATION_BACKENDS = (
#     'apps.utils.authentication.CustomAuthBackend',
# )
# REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'apps.utils.pagination.CustomPaginator',
    'PAGE_SIZE': 100

}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# LOGGING CONFIGURATION
LOGS_DIR = os.path.join(BASE_DIR, "../logs")
if not os.path.isdir(LOGS_DIR):
    os.mkdir(LOGS_DIR)
LOG_FORMAT = "[%(levelname)s][%(asctime)s]%(message)s - %(pathname)s#lines-%(lineno)s[%(funcName)s]"
LOG_DATE_FORMAT = "%d/%b/%Y %H:%M:%S"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": LOG_FORMAT,
            "datefmt": LOG_DATE_FORMAT,
        }
    },
    "handlers": {
        "finance_log_handler": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "finance.log"),
            "formatter": "standard",
            "maxBytes": 104857600,
        },
        "core_log_handler": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "core.log"),
            "formatter": "standard",
            "maxBytes": 104857600,
        },
    },
    "loggers": {
        "finance": {
            "handlers": ["finance_log_handler"],
            "level": "INFO",
            "propagate": True,
        },
        "core": {
            "handlers": ["core_log_handler"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# SWAGGER CONFIGURATION
LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        'basic': {
            'type': 'basic'
        }
    },
    "USE_SESSION_AUTH": True,
    "TAGS_SORTER": "alpha",
}

# For CORS and CSRF
CORS_ALLOW_HEADERS = list(default_headers) + ["X-Amz-Date"]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://192.168.8.103:8080",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
]
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
