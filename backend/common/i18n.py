from typing import Any

from starlette_context.errors import ContextDoesNotExistError

from backend.common.context import ctx
from backend.core.conf import settings
from backend.locale.loader import locale_loader


class I18n:
    """国际化管理器"""

    @property
    def current_language(self) -> str:
        """获取当前请求的语言"""
        try:
            return ctx.language
        except (AttributeError, LookupError, ContextDoesNotExistError):
            return settings.I18N_DEFAULT_LANGUAGE

    @current_language.setter
    def current_language(self, language: str) -> None:
        """设置当前请求的语言"""
        ctx.language = language

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
            translation = locale_loader.locales[self.current_language]
        except KeyError:
            keys = 'error.language_not_found'.split('.')
            translation = locale_loader.locales[settings.I18N_DEFAULT_LANGUAGE]

        for k in keys:
            if isinstance(translation, dict) and k in list(translation.keys()):
                translation = translation[k]
            else:
                # Pydantic 兼容
                translation = None if keys[0] == 'pydantic' else key
                break

        if translation and kwargs:
            translation = translation.format(**kwargs)

        return translation or default


# 创建 i18n 单例
i18n = I18n()

# 创建翻译函数实例
t = i18n.t
