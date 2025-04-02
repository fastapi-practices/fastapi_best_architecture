#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache

from pydantic_settings import BaseSettings


class ConfigSettings(BaseSettings):
    """参数配置"""

    # 参数
    CONFIG_BUILT_IN_TYPES: list[str] = ['website', 'protocol', 'policy']


@lru_cache
def get_config_settings() -> ConfigSettings:
    """获取参数配置"""
    return ConfigSettings()


config_settings = get_config_settings()
