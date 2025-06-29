#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.5.2'

from backend.utils.console import console


def get_version() -> str | None:
    console.print(f'[cyan]{__version__}[/]')
