"""
Django settings for crawlsy project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "daphne",
    # 'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "channels",
    "django_celery_beat",
    "apps.User",
    "apps.Node",
    "apps.Task",
    "apps.Spider",
    "apps.Ide",
    "apps.Alerts",
    "apps.Monitor",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "utils.middleware.UserOperationLogMiddleware",  # 添加用户操作日志中间件
]

ROOT_URLCONF = "crawlsy.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "crawlsy.wsgi.application"

# django-channels
ASGI_APPLICATION = "crawlsy.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DB_NAME"),
        "USER": os.getenv("MYSQL_DB_USER"),
        "PASSWORD": os.getenv("MYSQL_DB_PASSWORD"),
        "HOST": os.getenv("MYSQL_DB_HOST"),
        "PORT": os.getenv("MYSQL_DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("DEFAULT_REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "access_token": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("ACCESS_TOKEN_REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "refresh_token": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REFRESH_TOKEN_REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

# Password hasher
PASSWORD_HASHERS = {
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
}

# JWT
TOKEN_ISS = os.getenv("TOKEN_ISS", "SpiderStudio-ISS@2024")
REFRESH_TOKEN_OUT_TIME = int(os.getenv("REFRESH_TOKEN_OUT_TIME", 60 * 60 * 24))  # 默认24小时
ACCESS_TOKEN_OUT_TIME = int(os.getenv("ACCESS_TOKEN_OUT_TIME", 60))              # 默认60秒

# CORS
CORS_ORIGIN_ALLOW_ALL = os.getenv('CORS_ORIGIN_ALLOW_ALL', 'true').lower() == 'true'
CORS_ALLOW_METHODS = os.getenv('CORS_ALLOW_METHODS', '*').split(',')  # 用逗号分隔的字符串
CORS_ALLOW_CREDENTIALS = os.getenv('CORS_ALLOW_CREDENTIALS', 'true').lower() == 'true'
CORS_ALLOW_HEADERS = os.getenv('CORS_ALLOW_HEADERS', '*').split(',')  # 用逗号分隔的字符串

# 如果需要指定允许的源，可以添加
# CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '*').split(',')

# REST
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "utils.exception_handler.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "utils.pagination.CustomPagination",
    "PAGE_SIZE": int(os.getenv('PAGE_SIZE', 10)),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # 匿名用户与认证设置为None
    "UNAUTHENTICATED_USER": None,
    "UNAUTHENTICATED_TOKEN": None,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "utils.auth.CustomLoginAuth",
    ],
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    "DEFAULT_PERMISSION_CLASSES": [
        "utils.auth.CustomPermission",
    ],
}

# Swagger
SPECTACULAR_SETTINGS = {
    "TITLE": "爬虫管理平台API",
    "DESCRIPTION": "爬虫管理平台API文档",
    "SERVE_INCLUDE_SCHEMA": False,
    # 'SCHEMA_PATH_PREFIX': None,
    # 或者如果有统一的前缀，可以设置成
    "SCHEMA_PATH_PREFIX": "/api/V1/",
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
}

# Log
LOGGING_PATH = Path("/var/log/") / "SpiderStudio.log"
LOGGING_PATH.parent.mkdir(exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # 设置已存在的logger不失效
    "filters": {},
    "formatters": {
        "standard": {
            "format": "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d:%(funcName)s]：%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "[%(asctime)s][%(levelname)s]：%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
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
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "default": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGGING_PATH,
            "maxBytes": 1024 * 1024 * 20,  # 日志大小20M
            "backupCount": 5,
            "formatter": "standard",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "django": {
            "handlers": [
                "console",
                "default",
            ],  # 'email_handler'],
            "level": "INFO",
            "propagate": True,
        }
    },
}

# Ide resources
IDE_ROOT = Path("/data")
IDE_RESOURCES = IDE_ROOT / "spider_project"
IDE_MAX_FILE_SIZE = int(os.getenv('IDE_MAX_FILE_SIZE', 1024 * 1024 * 10))
IDE_TEMP = IDE_ROOT / "spider_temp"

# Celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELWRY_WORKER_CONCURRENCY = int(os.getenv('CELERY_WORKER_CONCURRENCY', 1))
CELERY_WORKER_MAX_TASKS_PER_CHILD = int(os.getenv('CELERY_WORKER_MAX_TASKS_PER_CHILD', 50))

# Node Service
NODE_SERVICE_URL = os.getenv("NODE_SERVICE_URL")

# MongoDB
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")

APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")
CARD_ID = os.getenv("FEISHU_CARD_ID")
CARD_VERSION = os.getenv("FEISHU_CARD_VERSION")

# Callback
FRONT_END_ADDRESS = os.getenv("FRONT_END_ADDRESS")