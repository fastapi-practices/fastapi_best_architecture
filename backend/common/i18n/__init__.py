#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国际化(i18n)模块

支持多语言的翻译系统
"""

from .manager import I18nManager, get_i18n_manager
from .middleware import I18nMiddleware

__all__ = ['I18nManager', 'get_i18n_manager', 'I18nMiddleware']
