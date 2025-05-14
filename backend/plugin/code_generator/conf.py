#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache

from pydantic_settings import BaseSettings


class GeneratorSettings(BaseSettings):
    """Code Generation Configuration"""

    # Code Download
    DOWNLOAD_ZIP_FILENAME: str = 'fba_generator'


@lru_cache
def get_generator_settings() -> GeneratorSettings:
    """Get Code Generation Configuration"""
    return GeneratorSettings()


generator_settings = get_generator_settings()
