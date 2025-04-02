#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.core.path_conf import BASE_PATH


class AdminSettings(BaseSettings):
    """Admin 配置"""

    model_config = SettingsConfigDict(env_file=f'{BASE_PATH}/.env', env_file_encoding='utf-8', extra='ignore')

    # .env OAuth2
    OAUTH2_GITHUB_CLIENT_ID: str
    OAUTH2_GITHUB_CLIENT_SECRET: str
    OAUTH2_LINUX_DO_CLIENT_ID: str
    OAUTH2_LINUX_DO_CLIENT_SECRET: str

    # OAuth2
    OAUTH2_GITHUB_REDIRECT_URI: str = 'http://127.0.0.1:8000/api/v1/oauth2/github/callback'
    OAUTH2_LINUX_DO_REDIRECT_URI: str = 'http://127.0.0.1:8000/api/v1/oauth2/linux-do/callback'
    OAUTH2_FRONTEND_REDIRECT_URI: str = 'http://localhost:5173/oauth2/callback'

    # 验证码
    CAPTCHA_LOGIN_REDIS_PREFIX: str = 'fba:login:captcha'
    CAPTCHA_LOGIN_EXPIRE_SECONDS: int = 60 * 5  # 3 分钟


@lru_cache
def get_admin_settings() -> AdminSettings:
    """获取 admin 配置"""
    return AdminSettings()


admin_settings = get_admin_settings()
