#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.utils.console import console

__version__ = '1.6.0'


def get_version() -> str | None:
    console.print(f'[cyan]{__version__}[/]')
