#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache
from typing import Any, Literal

from celery.schedules import crontab
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.core.path_conf import BASE_PATH


class Settings(BaseSettings):
    """Global Configuration"""

    model_config = SettingsConfigDict(
        env_file=f'{BASE_PATH}/.env',
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=True,
    )

    # .env environment
    ENVIRONMENT: Literal['dev', 'pro']

    # .env database
    DATABASE_TYPE: Literal['mysql', 'postgresql']
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    # .env Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DATABASE: int

    # .env Token
    TOKEN_SECRET_KEY: str  # Key secrets.token_urlsafe(32)

    # .env operation log encryption key
    # key os.urandom(32), to be converted to bytes.hex() str
    OPERA_LOG_ENCRYPT_SECRET_KEY: str

    # FastAPI
    FASTAPI_API_V1_PATH: str = '/api/v1'
    FASTAPI_TITLE: str = 'FastAPI'
    FASTAPI_VERSION: str = '0.0.1'
    FASTAPI_DESCRIPTION: str = 'FastAPI Best Architecture'
    FASTAPI_DOCS_URL: str = '/docs'
    FASTAPI_REDOC_URL: str = '/redoc'
    FASTAPI_OPENAPI_URL: str | None = '/openapi'
    FASTAPI_STATIC_FILES: bool = True

    # Database
    DATABASE_ECHO: bool = False
    DATABASE_POOL_ECHO: bool = False
    DATABASE_SCHEMA: str = 'fba'
    DATABASE_CHARSET: str = 'utf8mb4'

    # Redis
    REDIS_TIMEOUT: int = 5

    # Token
    TOKEN_ALGORITHM: str = 'HS256'
    TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24  # 1 Day
    TOKEN_REFRESH_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 days
    TOKEN_REDIS_PREFIX: str = 'fba:token'
    TOKEN_EXTRA_INFO_REDIS_PREFIX: str = 'fba:token_extra_info'
    TOKEN_ONLINE_REDIS_PREFIX: str = 'fba:token_online'
    TOKEN_REFRESH_REDIS_PREFIX: str = 'fba:refresh_token'
    TOKEN_REQUEST_PATH_EXCLUDE: list[str] = [  # JWT / RBAC ROUTE WHITE LIST
        f'{FASTAPI_API_V1_PATH}/auth/login',
    ]

    # JWT
    JWT_USER_REDIS_PREFIX: str = 'fba:user'
    JWT_USER_REDIS_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 days

    # RBAC
    RBAC_ROLE_MENU_MODE: bool = True
    RBAC_ROLE_MENU_EXCLUDE: list[str] = [
        'sys:monitor:redis',
        'sys:monitor:server',
    ]

    # Cookie
    COOKIE_REFRESH_TOKEN_KEY: str = 'fba_refresh_token'
    COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 days

    # Data Permission Configuration
    DATA_PERMISSION_MODELS: dict[str, str] = {  # SQLA MODEL ALLOWING DATA FILTERING, WHICH MUST BE DEFINED BY A MODULAR STRING
        'Sector': 'backend.app.admin.model.Dept',
    }
    DATA_PERMISSION_COLUMN_EXCLUDE: list[str] = [  # EXCLUDES SQLA MODEL COLUMNS THAT ALLOW DATA FILTERING
        'id',
        'sort',
        'del_flag',
        'created_time',
        'updated_time',
    ]

    # Socket.IO
    WS_NO_AUTH_MARKER: str = 'internal'

    # CORS
    CORS_ALLOWED_ORIGINS: list[str] = [  # No slash at the end
        'http://127.0.0.1:8000',
        'http://localhost:5173',
    ]
    CORS_EXPOSE_HEADERS: list[str] = [
        'X-Request-ID',
    ]

    # Intermediate Configuration
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_ACCESS: bool = True

    # Request restricted configuration
    REQUEST_LIMITER_REDIS_PREFIX: str = 'fba:limiter'

    # Time Configuration
    DATETIME_TIMEZONE: str = 'Asia/Shanghai'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'

    # Uploading files
    UPLOAD_READ_SIZE: int = 1024
    UPLOAD_IMAGE_EXT_INCLUDE: list[str] = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    UPLOAD_IMAGE_SIZE_MAX: int = 5 * 1024 * 1024  # 5 MB
    UPLOAD_VIDEO_EXT_INCLUDE: list[str] = ['mp4', 'mov', 'avi', 'flv']
    UPLOAD_VIDEO_SIZE_MAX: int = 20 * 1024 * 1024  # 20 MB

    # Presentation Mode Configuration
    DEMO_MODE: bool = False
    DEMO_MODE_EXCLUDE: set[tuple[str, str]] = {
        ('POST', f'{FASTAPI_API_V1_PATH}/auth/login'),
        ('POST', f'{FASTAPI_API_V1_PATH}/auth/logout'),
        ('GET', f'{FASTAPI_API_V1_PATH}/auth/captcha'),
    }

    # IP POSITION CONFIGURATION
    IP_LOCATION_PARSE: Literal['online', 'offline', 'false'] = 'offline'
    IP_LOCATION_REDIS_PREFIX: str = 'fba:ip:location'
    IP_LOCATION_EXPIRE_SECONDS: int = 60 * 60 * 24  # 1 Day

    # Tracking ID
    TRACE_ID_REQUEST_HEADER_KEY: str = 'X-Request-ID'

    # Log
    LOG_CID_DEFAULT_VALUE: str = '-'
    LOG_CID_UUID_LENGTH: int = 32  # log profile_id length, must be less than equal 32
    LOG_STD_LEVEL: str = 'INFO'
    LOG_ACCESS_FILE_LEVEL: str = 'INFO'
    LOG_ERROR_FILE_LEVEL: str = 'ERROR'
    LOG_STD_FORMAT: str = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | '
        '<cyan> {correlation_id} </> | <lvl>{message}</>'
    )
    LOG_FILE_FORMAT: str = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | '
        '<cyan> {correlation_id} </> | <lvl>{message}</>'
    )
    LOG_ACCESS_FILENAME: str = 'fba_access.log'
    LOG_ERROR_FILENAME: str = 'fba_error.log'

    # Operation Log
    OPERA_LOG_PATH_EXCLUDE: list[str] = [
        '/favicon.ico',
        '/docs',
        '/redoc',
        '/openapi',
        f'{FASTAPI_API_V1_PATH}/auth/login/swagger',
        f'{FASTAPI_API_V1_PATH}/oauth2/github/callback',
        f'{FASTAPI_API_V1_PATH}/oauth2/linux-do/callback',
    ]
    # 0: AES (performance loss); 1: md5; 2: ItsDangerous; 3: Unencrypted, others: replace with ******
    OPERA_LOG_ENCRYPT_TYPE: int = 1
    OPERA_LOG_ENCRYPT_KEY_INCLUDE: list[str] = [  # Encrypted interface into the values corresponding to the parameters
        'password',
        'old_password',
        'new_password',
        'confirm_password',
    ]

    # Plugin Configuration
    PLUGIN_PIP_CHINA: bool = True
    PLUGIN_PIP_INDEX_URL: str = 'https://mirrors.aliyun.com/pypi/simple/'

    # App Admin
    # .env OAuth2
    OAUTH2_GITHUB_CLIENT_ID: str
    OAUTH2_GITHUB_CLIENT_SECRET: str
    OAUTH2_LINUX_DO_CLIENT_ID: str
    OAUTH2_LINUX_DO_CLIENT_SECRET: str

    # OAuth2
    OAUTH2_FRONTEND_REDIRECT_URI: str = 'http://localhost:5173/oauth2/callback'

    # 验证码
    CAPTCHA_LOGIN_REDIS_PREFIX: str = 'fba:login:captcha'
    CAPTCHA_LOGIN_EXPIRE_SECONDS: int = 60 * 5  # 3 分钟

    # App Task
    # .env Redis 配置
    CELERY_BROKER_REDIS_DATABASE: int
    CELERY_BACKEND_REDIS_DATABASE: int

    # .env RabbitMQ 配置
    # docker run -d --hostname fba-mq --name fba-mq  -p 5672:5672 -p 15672:15672 rabbitmq:latest
    CELERY_RABBITMQ_HOST: str
    CELERY_RABBITMQ_PORT: int
    CELERY_RABBITMQ_USERNAME: str
    CELERY_RABBITMQ_PASSWORD: str

    # 基础配置
    CELERY_BROKER: Literal['rabbitmq', 'redis'] = 'redis'
    CELERY_BACKEND_REDIS_PREFIX: str = 'fba:celery:'
    CELERY_BACKEND_REDIS_TIMEOUT: int = 5
    CELERY_TASK_PACKAGES: list[str] = [
        'app.task.celery_task',
        'app.task.celery_task.db_log',
    ]
    CELERY_TASK_MAX_RETRIES: int = 5

    # 定时任务配置
    CELERY_SCHEDULE: dict[str, dict[str, Any]] = {
        'exec-every-10-seconds': {
            'task': 'task_demo_async',
            'schedule': 10,
        },
        'exec-every-sunday': {
            'task': 'delete_db_opera_log',
            'schedule': crontab('0', '0', day_of_week='6'),
        },
        'exec-every-15-of-month': {
            'task': 'delete_db_login_log',
            'schedule': crontab('0', '0', day_of_month='15'),
        },
    }

    # Plugin Code Generator
    # 代码下载
    CODE_GENERATOR_DOWNLOAD_ZIP_FILENAME: str = 'fba_generator'

    # Plugin Config
    # 参数配置
    CONFIG_BUILT_IN_TYPES: list[str] = ['website', 'protocol', 'policy']

    @model_validator(mode='before')
    @classmethod
    def check_env(cls, values: Any) -> Any:
        """Disable OpenAPI documents and static file services in production environment"""
        if values.get('ENVIRONMENT') == 'pro':
            # FastAPI
            values['FASTAPI_OPENAPI_URL'] = None
            values['FASTAPI_STATIC_FILES'] = False
            # Task
            values['CELERY_BROKER'] = 'rabbitmq'

        return values


@lru_cache
def get_settings() -> Settings:
    """Get a global configuration case"""
    return Settings()


# Create global configuration instance
settings = get_settings()
