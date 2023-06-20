#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


class CustomCode(Enum):
    """
    自定义错误码
    """

    CAPTCHA_ERROR = (40001, '验证码错误')

    @property
    def code(self):
        """
        获取错误码
        """
        return self.value[0]

    @property
    def msg(self):
        """
        获取错误码码信息
        """
        return self.value[1]
