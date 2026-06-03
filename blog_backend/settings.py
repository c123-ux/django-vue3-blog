"""
Django settings for blog_backend project.
个人博客系统 - 开发环境配置
"""

from pathlib import Path
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

# 前端地址（OAuth 回调跳转）
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_spectacular',
    'django_filters',
    
    # WebSocket (需要 ASGI 支持，开发环境可注释)
    # 'channels',
    
    # Performance monitoring
    # 'django_prometheus',
    
    # Local apps
    'apps.users',
    'apps.articles',
    'apps.comments',
    'apps.system',
    'apps.notes',
    'apps.monitoring',
]

MIDDLEWARE = [
    # 'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'blog_backend.urls'

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

WSGI_APPLICATION = 'blog_backend.wsgi.application'


# Database
# 开发环境使用 SQLite，生产环境切换到 PostgreSQL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 生产环境 PostgreSQL 配置示例（取消注释并使用环境变量）
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'blog_db'),
#         'USER': os.environ.get('DB_USER', 'blog_user'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', ''),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'zh-hans'  # 中文
TIME_ZONE = 'Asia/Shanghai'  # 中国时区
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (用户上传的文件)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django REST Framework 配置

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/hour',
        'user': '5000/hour',
        'login': '10/min',
        'comment': '30/min',
        'upload': '20/min',
    },
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# JWT 配置

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # Access Token 30分钟过期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),      # Refresh Token 7天过期
    'ROTATE_REFRESH_TOKENS': True,                    # 刷新时轮换 Refresh Token
    'BLACKLIST_AFTER_ROTATION': True,                 # 旧 Token 加入黑名单
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# CORS 配置（前后端分离必需）

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite 默认端口
    "http://127.0.0.1:5173",
    "http://localhost:5174",  # 另一个常用端口
    "http://127.0.0.1:5174",
]

CORS_ALLOW_CREDENTIALS = True

# Redis 缓存配置
# 如果没有 Redis，可以使用内存缓存（开发环境）

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# 缓存超时时间（秒）
CACHE_TTL = {
    'article_detail': 600,  # 文章详情缓存 10 分钟
    'article_list': 300,    # 文章列表缓存 5 分钟
}

# drf-spectacular API 文档配置

SPECTACULAR_SETTINGS = {
    'TITLE': '个人博客 API',
    'DESCRIPTION': '基于 Django + DRF + Vue3 的个人博客系统 API 文档',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}

# Celery 异步任务配置

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/2')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/2')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

# Celery 任务配置
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30分钟超时
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25分钟软超时

# Celery Beat调度配置 - 定时任务
# 如果没有安装 Celery，定时任务功能将被禁用
try:
    from celery.schedules import crontab
    
    CELERY_BEAT_SCHEDULE = {
        # 每天凌晨2点执行文章统计
        'update-article-statistics': {
            'task': 'apps.articles.tasks.update_article_statistics',
            'schedule': crontab(hour=2, minute=0),  # 每天凌晨2点
        },
        
        # 每小时执行缓存清理
        'cleanup-old-cache': {
            'task': 'apps.articles.tasks.cleanup_old_cache',
            'schedule': crontab(minute=0),  # 每小时整点
        },
        
        # 每天早上8点生成日报
        'generate-daily-report': {
            'task': 'apps.articles.tasks.generate_daily_report',
            'schedule': crontab(hour=8, minute=0),  # 每天早上8点
        },
        
        # 每天晚上11点清理临时文件
        'cleanup-temp-files': {
            'task': 'apps.articles.tasks.cleanup_temp_files',
            'schedule': crontab(hour=23, minute=0),  # 每天晚上11点
        },
        
        # 每周一上午9点发送周报
        'send-weekly-digest': {
            'task': 'apps.articles.tasks.send_weekly_digest',
            'schedule': crontab(hour=9, minute=0, day_of_week=1),  # 每周一上午9点
        },
    }
except ImportError:
    CELERY_BEAT_SCHEDULE = {}
    print("[WARN] Celery not installed, scheduled tasks disabled")

# 日志配置

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
        # 'json': {
        #     '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        #     'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        # },
        # 如需 JSON 日志格式，请安装 python-json-logger
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'error.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# 创建日志目录
import logging
import sys
from pathlib import Path

log_dir = BASE_DIR / 'logs'
if not log_dir.exists():
    log_dir.mkdir(exist_ok=True)

# WebSocket 配置

# ASGI_APPLICATION = 'blog_backend.asgi.application'

CHANNEL_LAYERS = {}

# 邮件配置（使用 Anymail）

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # 开发环境打印到控制台

# 生产环境邮件配置示例
# EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
# ANYMAIL = {
#     'SENDGRID_API_KEY': os.environ.get('SENDGRID_API_KEY'),
# }

DEFAULT_FROM_EMAIL = 'noreply@blog.com'

# Sentry 错误追踪配置（生产环境）

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
# 
# sentry_sdk.init(
#     dsn=os.environ.get('SENTRY_DSN'),
#     integrations=[DjangoIntegration()],
#     traces_sample_rate=1.0,
#     send_default_pii=False
# )

# 文件上传配置

FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Elasticsearch 配置（可选）
# 如果没有安装 Elasticsearch，将 'django_elasticsearch_dsl' 从 INSTALLED_APPS 中移除

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': os.environ.get('ELASTICSEARCH_HOSTS', 'http://localhost:9200').split(','),
        'timeout': 20,
    },
}

# Elasticsearch 索引设置
ELASTICSEARCH_INDEX_NAMES = {
    'apps.articles.documents.ArticleDocument': 'articles',
}

USE_ELASTICSEARCH = os.environ.get('USE_ELASTICSEARCH', 'false').lower() == 'true'

# Prometheus 监控
ENABLE_PROMETHEUS_METRICS = os.environ.get('ENABLE_PROMETHEUS_METRICS', 'true').lower() == 'true'

# 定义默认分页类
REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = 'rest_framework.pagination.PageNumberPagination'
REST_FRAMEWORK['PAGE_SIZE'] = 10

# 安全配置（生产环境）

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True