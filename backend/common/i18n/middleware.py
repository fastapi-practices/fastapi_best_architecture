#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from contextvars import ContextVar
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .manager import get_i18n_manager

# 上下文变量，用于在请求中存储当前语言
current_language: ContextVar[str] = ContextVar('current_language', default='zh-CN')


class I18nMiddleware(BaseHTTPMiddleware):
    """国际化中间件"""

    def __init__(self, app, default_language: str = 'zh-CN'):
        super().__init__(app)
        self.default_language = default_language
        self.i18n_manager = get_i18n_manager()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求，设置语言"""

        # 从多个来源检测语言偏好
        language = self._detect_language(request)

        # 设置上下文变量
        current_language.set(language)

        # 设置管理器的默认语言
        self.i18n_manager.set_language(language)

        # 继续处理请求
        response = await call_next(request)

        # 可选：在响应头中添加语言信息
        response.headers['Content-Language'] = language

        return response

    def _detect_language(self, request: Request) -> str:
        """检测请求的语言偏好"""

        # 1. 优先检查 URL 参数
        lang_param = request.query_params.get('lang')
        if lang_param and lang_param in self.i18n_manager.supported_languages:
            return lang_param

        # 2. 检查请求头中的自定义语言字段
        lang_header = request.headers.get('X-Language')
        if lang_header and lang_header in self.i18n_manager.supported_languages:
            return lang_header

        # 3. 检查 Accept-Language 头
        accept_language = request.headers.get('Accept-Language', '')
        if accept_language:
            # 简单解析 Accept-Language，取第一个支持的语言
            languages = [lang.strip().split(';')[0] for lang in accept_language.split(',')]
            for lang in languages:
                # 处理语言代码的变体，如 'en' -> 'en-US', 'zh' -> 'zh-CN'
                normalized_lang = self._normalize_language(lang)
                if normalized_lang in self.i18n_manager.supported_languages:
                    return normalized_lang

        # 4. 返回默认语言
        return self.default_language

    @staticmethod
    def _normalize_language(lang: str) -> str:
        """规范化语言代码"""
        lang = lang.lower().strip()

        # 语言映射
        lang_mapping = {
            'zh': 'zh-CN',
            'zh-cn': 'zh-CN',
            'zh-hans': 'zh-CN',
            'en': 'en-US',
            'en-us': 'en-US',
        }

        return lang_mapping.get(lang, lang)


def get_current_language() -> str:
    """获取当前请求的语言"""
    return current_language.get('zh-CN')
