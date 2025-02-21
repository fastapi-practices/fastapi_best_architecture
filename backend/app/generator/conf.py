#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache

from pydantic_settings import BaseSettings


class GeneratorSettings(BaseSettings):
    """Admin Settings"""

    # 模版目录
    TEMPLATE_BACKEND_DIR_NAME: str = 'py'

    # 代码下载
    DOWNLOAD_ZIP_FILENAME: str = 'fba_generator'


@lru_cache
def get_generator_settings() -> GeneratorSettings:
    """获取 generator 配置"""
    return GeneratorSettings()


generator_settings = get_generator_settings()
