#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.common.i18n import i18n
from backend.utils.console import console

__version__ = '1.8.0'


def get_version() -> str | None:
    console.print(f'[cyan]{__version__}[/]')


# 初始化 i18n
i18n.load_locales()
