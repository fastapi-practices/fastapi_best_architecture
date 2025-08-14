#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import json
import os

from pathlib import Path
from typing import Any

import yaml

from backend.core.conf import settings
from backend.core.path_conf import LOCALE_DIR


class I18n:
    """国际化管理器"""

    def __init__(self):
        self.locales: dict[str, dict[str, Any]] = {}
        self.current_language: str = settings.I18N_DEFAULT_LANGUAGE

    def load_locales(self):
        """加载语言文本"""
        patterns = [
            os.path.join(LOCALE_DIR, '*.json'),
            os.path.join(LOCALE_DIR, '*.yaml'),
            os.path.join(LOCALE_DIR, '*.yml'),
        ]

        lang_files = []

        for pattern in patterns:
            lang_files.extend(glob.glob(pattern))

        for lang_file in lang_files:
            with open(lang_file, 'r', encoding='utf-8') as f:
                lang = Path(lang_file).stem
                file_type = Path(lang_file).suffix[1:]
                match file_type:
                    case 'json':
                        self.locales[lang] = json.loads(f.read())
                    case 'yaml' | 'yml':
                        self.locales[lang] = yaml.full_load(f.read())

    def t(self, key: str, default: Any | None = None, **kwargs) -> str:
        """
        翻译函数

        :param key: 目标文本键，支持点分隔，例如 'response.success'
        :param default: 目标语言文本不存在时的默认文本
        :param kwargs: 目标文本中的变量参数
        :return:
        """
        keys = key.split('.')

        try:
            translation = self.locales[self.current_language]
        except KeyError:
            keys = 'error.language_not_found'
            translation = self.locales[settings.I18N_DEFAULT_LANGUAGE]

        for k in keys:
            if isinstance(translation, dict) and k in list(translation.keys()):
                translation = translation[k]
            else:
                # Pydantic 兼容
                if keys[0] == 'pydantic':
                    translation = None
                else:
                    translation = key

        if translation and kwargs:
            translation = translation.format(**kwargs)

        return translation or default


# 创建 i18n 单例
i18n = I18n()

# 创建翻译函数实例
t = i18n.t
