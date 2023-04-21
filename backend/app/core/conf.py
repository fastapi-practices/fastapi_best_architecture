#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    ENVIRONMENT: str
    # FastAPI
    TITLE: str = 'FastAPI'
    VERSION: str = 'v0.0.1'
    DESCRIPTION: str = "FastAPI Best Architecture"
    DOCS_URL: Optional[str] = '/v1/docs'
    REDOCS_URL: Optional[str] = '/v1/redocs'
    OPENAPI_URL: Optional[str] = '/v1/openapi'

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

    # MySQL
    DB_ECHO: bool = False
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_DATABASE: str = 'fba'
    DB_CHARSET: str = 'utf8mb4'

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DATABASE: int
    REDIS_TIMEOUT: int = 5

    # APScheduler DB
    APS_REDIS_HOST: str
    APS_REDIS_PORT: int
    APS_REDIS_PASSWORD: str
    APS_REDIS_DATABASE: int = 1
    APS_REDIS_TIMEOUT: int = 10

    # APScheduler Default
    APS_COALESCE: bool = False  # 是否合并运行
    APS_MAX_INSTANCES: int = 3  # 最大实例数
    APS_MISFIRE_GRACE_TIME: int = 60  # 任务错过执行时间后，最大容错时间，过期后不再执行，单位：秒

    # Token
    TOKEN_ALGORITHM: str = 'HS256'  # 算法
    TOKEN_SECRET_KEY: str  # 密钥 secrets.token_urlsafe(32))
    TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # token 时效 60 * 24 * 1 = 1 天
    TOKEN_URL: str = '/v1/users/login'

    # Email
    EMAIL_DESCRIPTION: str = 'fastapi_sqlalchemy_mysql'  # 默认发件说明
    EMAIL_SERVER: str = 'smtp.qq.com'
    EMAIL_PORT: int = 465
    EMAIL_USER: str
    EMAIL_PASSWORD: str  # 授权密码，非邮箱密码
    EMAIL_SSL: bool = True  # 是否使用ssl

    # 邮箱登录验证码过期时间
    EMAIL_LOGIN_CODE_MAX_AGE: int = 60 * 2  # 时效 60 * 2 = 2 分钟

    # Cookies
    COOKIES_MAX_AGE: int = 60 * 5  # cookies 时效 60 * 5 = 5 分钟

    # Middleware
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_GZIP: bool = True
    MIDDLEWARE_ACCESS: bool = False

    class Config:
        env_file = '.env'


@lru_cache
def get_settings():
    """ 读取配置优化写法 """
    return Settings()


settings = get_settings()
