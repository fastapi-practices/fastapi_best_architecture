#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def search_string(pattern, text) -> bool:
    """
    全字段正则匹配

    :param pattern:
    :param text:
    :return:
    """
    result = re.search(pattern, text)
    if result:
        return True
    else:
        return False


def match_string(pattern, text) -> bool:
    """
    从字段开头正则匹配

    :param pattern:
    :param text:
    :return:
    """
    result = re.match(pattern, text)
    if result:
        return True
    else:
        return False


def is_phone(text: str) -> bool:
    """
    检查手机号码

    :param text:
    :return:
    """
    return match_string(r'^1[3-9]\d{9}$', text)
