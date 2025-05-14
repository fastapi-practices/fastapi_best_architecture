#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def search_string(pattern: str, text: str) -> bool:
    """
    All Fields Regular Match

    :param pattern: regular expression mode
    :param text: to be matched
    :return:
    """
    if not pattern or not text:
        return False

    result = re.search(pattern, text)
    return result is not None


def match_string(pattern: str, text: str) -> bool:
    """
    Match regular from the beginning of the field

    :param pattern: regular expression mode
    :param text: to be matched
    :return:
    """
    if not pattern or not text:
        return False

    result = re.match(pattern, text)
    return result is not None


def is_phone(text: str) -> bool:
    """
    Check cell phone number format

    :param text: cell phone number to be checked
    :return:
    """
    if not text:
        return False

    phone_pattern = r'^1[3-9]\d{9}$'
    return match_string(phone_pattern, text)
