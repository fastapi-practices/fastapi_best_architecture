#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def search_string(pattern: str, text: str) -> bool:
    """
    全字段正则匹配

    :param pattern: 正则表达式模式
    :param text: 待匹配的文本
    :return:
    """
    if not pattern or not text:
        return False

    result = re.search(pattern, text)
    return result is not None


def match_string(pattern: str, text: str) -> bool:
    """
    从字段开头正则匹配

    :param pattern: 正则表达式模式
    :param text: 待匹配的文本
    :return:
    """
    if not pattern or not text:
        return False

    result = re.match(pattern, text)
    return result is not None


def is_phone(text: str) -> bool:
    """
    检查手机号码格式

    :param text: 待检查的手机号码
    :return:
    """
    if not text:
        return False

    phone_pattern = r'^1[3-9]\d{9}$'
    return match_string(phone_pattern, text)
