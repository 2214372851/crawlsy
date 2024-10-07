"""
Django settings for spiderManage project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6wdw3s$j5$^a*f%2tn0bqrrit=b2_pxqo4^()usrr=a0^dpgka'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'drf_yasg',

    'apps.User',
    'apps.Node',
    'apps.Task',
    'apps.Spider',
    'apps.Ide',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'spiderManage.urls'

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

WSGI_APPLICATION = 'spiderManage.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SpiderManage',
        'USER': 'SpiderManage',
        'PASSWORD': 'hYJmTmt422KYzEde',
        'HOST': '8.153.17.121',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:redis_pCd7ts@8.153.17.121:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "access_token": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:redis_pCd7ts@8.153.17.121:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "refresh_token": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:redis_pCd7ts@8.153.17.121:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "node_detection": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:redis_pCd7ts@8.153.17.121:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Password hasher
PASSWORD_HASHERS = {
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher'
}

# JWT
TOKEN_ISS = 'SpiderStudio-ISS@2024'
REFRESH_TOKEN_OUT_TIME = 60 * 60 * 24
ACCESS_TOKEN_OUT_TIME = 60 * 60

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = ["*"]  # 配置允许的请求方式
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']

# REST
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.exception_handler.custom_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.CustomPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # 匿名用户与认证设置为None
    "UNAUTHENTICATED_USER": None,
    "UNAUTHENTICATED_TOKEN": None,
    # 'DEFAULT_AUTHENTICATION_CLASSES': ['utils.auth.CustomLoginAuth', ],
    # 'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
}

# Swagger
SWAGGER_SETTINGS = {
    'PERSIST_AUTH': True,
    'REFETCH_SCHEMA_WITH_AUTH': True,
    'REFETCH_SCHEMA_ON_LOGOUT': True,

    'SECURITY_DEFINITIONS': {
        'JWT': {
            'type': 'apiKey',
            'name': 'token',
            'in': 'header'
        },
        'RefreshToken': {
            'type': 'apiKey',
            'name': 'refresh-token',
            'in': 'header'
        }
    }
}

# Log
LOGGING_PATH = BASE_DIR / 'log' / 'SpiderStudio.log'
LOGGING_PATH.parent.mkdir(exist_ok=True)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 设置已存在的logger不失效
    'filters': {},
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d:%(funcName)s]：%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '[%(asctime)s][%(levelname)s]：%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        # 'email_handler': {
        #     'level': 'ERROR',
        #     'class': 'logging.handlers.SMTPHandler',
        #     'formatter': 'standard',
        #     'mailhost': (EMAIL_HOST, EMAIL_PORT),
        #     'fromaddr': 'Maadaa error<info@maadaa.ai>',
        #     'toaddrs': ['2214372851@qq.com'],
        #     'subject': 'SERVER错误',
        #     'credentials': (EMAIL_HOST_USER, EMAIL_HOST_PASSWORD),
        # },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_PATH,
            'maxBytes': 1024 * 1024 * 20,  # 日志大小20M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'default', ],  # 'email_handler'],
            'level': 'INFO',
            'propagate': True
        }
    },
}

# Ide resources
IDE_RESOURCES = Path('/data/spider_project')
IDE_MAX_FILE_SIZE = 1024 * 1024 * 10
