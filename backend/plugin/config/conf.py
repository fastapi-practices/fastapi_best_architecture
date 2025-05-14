#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache

from pydantic_settings import BaseSettings


class ConfigSettings(BaseSettings):
    """Parameter Configuration"""

    # Parameters
    CONFIG_BUILT_IN_TYPES: list[str] = ['website', 'protocol', 'policy']


@lru_cache
def get_config_settings() -> ConfigSettings:
    """Get Parameter Configuration"""
    return ConfigSettings()


config_settings = get_config_settings()
