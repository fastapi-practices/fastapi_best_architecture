import glob
import json

from pathlib import Path
from typing import Any

import yaml

from backend.core.path_conf import LOCALE_DIR


class LocaleLoader:
    """语言文件加载器"""

    def __init__(self) -> None:
        self.locales: dict[str, dict[str, Any]] = {}
        self.load_locales()

    def load_locales(self) -> None:
        """加载语言文本"""
        patterns = [
            LOCALE_DIR / '*.json',
            LOCALE_DIR / '*.yaml',
            LOCALE_DIR / '*.yml',
        ]

        lang_files = []

        for pattern in patterns:
            lang_files.extend(glob.glob(str(pattern)))

        for lang_file in lang_files:
            with open(lang_file, encoding='utf-8') as f:
                lang = Path(lang_file).stem
                file_type = Path(lang_file).suffix[1:]
                match file_type:
                    case 'json':
                        self.locales[lang] = json.loads(f.read())
                    case 'yaml' | 'yml':
                        self.locales[lang] = yaml.full_load(f.read())


# 创建语言加载器单例
locale_loader = LocaleLoader()
