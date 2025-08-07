#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

from functools import lru_cache
from typing import Any, Dict

from backend.core.path_conf import BASE_PATH


class I18nManager:
    """国际化管理器"""

    def __init__(self):
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.default_language = 'zh-CN'
        self.supported_languages = ['zh-CN', 'en-US']
        self._load_translations()

    def _load_translations(self):
        """加载翻译文件"""
        translations_dir = os.path.join(BASE_PATH, 'common', 'i18n', 'locales')

        for lang in self.supported_languages:
            lang_file = os.path.join(translations_dir, f'{lang}.json')
            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[lang] = json.load(f)
            else:
                self.translations[lang] = {}

    def t(self, key: str, language: str = None, **kwargs) -> str:
        """
        翻译函数

        :param key: 翻译键，支持点号分隔的嵌套键，如 'response.success'
        :param language: 目标语言，如果不指定则使用默认语言
        :param kwargs: 格式化参数
        :return: 翻译后的文本
        """
        if language is None:
            language = self.default_language

        if language not in self.translations:
            language = self.default_language

        # 获取翻译文本
        translation = self._get_nested_value(self.translations[language], key)

        if translation is None:
            # 如果在指定语言中找不到，尝试默认语言
            if language != self.default_language:
                translation = self._get_nested_value(self.translations[self.default_language], key)

            # 如果仍然找不到，返回键名
            if translation is None:
                return key

        # 格式化参数
        if kwargs:
            try:
                return translation.format(**kwargs)
            except (KeyError, ValueError):
                return translation

        return translation

    @staticmethod
    def _get_nested_value(data: Dict[str, Any], key: str) -> str | None:
        """获取嵌套字典的值"""
        keys = key.split('.')
        current = data

        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None

        return current if isinstance(current, str) else None

    def set_language(self, language: str):
        """设置默认语言"""
        if language in self.supported_languages:
            self.default_language = language


# 全局单例实例
_i18n_manager = None


@lru_cache()
def get_i18n_manager() -> I18nManager:
    """获取国际化管理器实例"""
    global _i18n_manager
    if _i18n_manager is None:
        _i18n_manager = I18nManager()
    return _i18n_manager


# 便捷地翻译函数
def t(key: str, language: str = None, **kwargs) -> str:
    """便捷地翻译函数"""
    return get_i18n_manager().t(key, language, **kwargs)
