#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache
from typing import Literal

from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    # Env Config
    ENVIRONMENT: str

    # Env MySQL
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str

    # Env Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DATABASE: int

    # Env APScheduler Redis
    APS_REDIS_HOST: str
    APS_REDIS_PORT: int
    APS_REDIS_PASSWORD: str
    APS_REDIS_DATABASE: int

    # Env Token
    TOKEN_SECRET_KEY: str  # 密钥 secrets.token_urlsafe(32)

    # Env Opera Log
    OPERA_LOG_ENCRYPT_SECRET_KEY: str  # 密钥 os.urandom(32), 需使用 bytes.hex() 方法转换为 str

    # FastAPI
    API_V1_STR: str = '/v1'
    TITLE: str = 'FastAPI'
    VERSION: str = '0.0.1'
    DESCRIPTION: str = 'FastAPI Best Architecture'
    DOCS_URL: str | None = f'{API_V1_STR}/docs'
    REDOCS_URL: str | None = f'{API_V1_STR}/redocs'
    OPENAPI_URL: str | None = f'{API_V1_STR}/openapi'

    @root_validator
    def validator_api_url(cls, values):
        if values['ENVIRONMENT'] == 'pro':
            values['OPENAPI_URL'] = None
        return values

    # Uvicorn
    UVICORN_HOST: str = '127.0.0.1'
    UVICORN_PORT: int = 8000
    UVICORN_RELOAD: bool = True

    # Static Server
    STATIC_FILES: bool = False

    # Location Parse
    LOCATION_PARSE: Literal['online', 'offline', 'false'] = 'offline'

    # Limiter
    LIMITER_REDIS_PREFIX: str = 'fba_limiter'

    # MySQL
    DB_ECHO: bool = False
    DB_DATABASE: str = 'fba'
    DB_CHARSET: str = 'utf8mb4'

    # Redis
    REDIS_TIMEOUT: int = 5

    # APScheduler Redis
    APS_REDIS_TIMEOUT: int = 10

    # APScheduler Default
    APS_COALESCE: bool = False  # 是否合并运行
    APS_MAX_INSTANCES: int = 3  # 最大实例数
    APS_MISFIRE_GRACE_TIME: int = 60  # 任务错过执行时间后，最大容错时间，过期后不再执行，单位：秒

    # Token
    TOKEN_ALGORITHM: str = 'HS256'  # 算法
    TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1  # 过期时间，单位：秒
    TOKEN_REFRESH_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 刷新过期时间，单位：秒
    TOKEN_URL_SWAGGER: str = '/api/v1/auth/swagger_login'
    TOKEN_REDIS_PREFIX: str = 'fba_token'
    TOKEN_REFRESH_REDIS_PREFIX: str = 'fba_refresh_token'

    # Captcha
    CAPTCHA_LOGIN_REDIS_PREFIX: str = 'fba_login_captcha'
    CAPTCHA_LOGIN_EXPIRE_SECONDS: int = 60 * 5  # 过期时间，单位：秒

    # Log
    LOG_STDOUT_FILENAME: str = 'fba_access.log'
    LOG_STDERR_FILENAME: str = 'fba_error.log'

    # Middleware
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_GZIP: bool = True
    MIDDLEWARE_ACCESS: bool = False

    # Casbin
    CASBIN_RBAC_MODEL_NAME: str = 'rbac_model.conf'
    CASBIN_EXCLUDE: set[tuple[str, str]] = {
        ('POST', '/api/v1/auth/swagger_login'),
        ('POST', '/api/v1/auth/login'),
        ('POST', '/api/v1/auth/register'),
        ('GET', '/api/v1/auth/captcha'),
    }

    # Menu
    MENU_PERMISSION: bool = True  # 开启此功能后, Casbin 鉴权将失效
    MENU_EXCLUDE: list[str] = [
        'auth:swagger_login',
        'auth:login',
        'auth:register',
        'auth:captcha',
    ]

    # Opera log
    OPERA_LOG_EXCLUDE: list[str] = [
        '/favicon.ico',
        DOCS_URL,
        REDOCS_URL,
        OPENAPI_URL,
        '/api/v1/auth/swagger_login',
    ]
    OPERA_LOG_ENCRYPT: int = 1  # 请求入参加密, 0: AES (高性能损耗), 1: md5, 2: 不加密, other: 替换为 ******
    OPERA_LOG_ENCRYPT_INCLUDE: list[str] = ['password', 'old_password', 'new_password', 'confirm_password']

    class Config:
        # https://docs.pydantic.dev/usage/settings/#dotenv-env-support
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings():
    """读取配置优化写法"""
    return Settings()


settings = get_settings()
