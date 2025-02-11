#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib

from functools import lru_cache
from typing import Any


def module_parse(module_path: str) -> tuple:
    """
    Parse a module string into a Python module and class/function.

    :param module_path:
    :return:
    """
    module_name, class_or_func = module_path.rsplit('.', 1)
    return module_name, class_or_func


@lru_cache(maxsize=512)
def import_module_cached(module_name: str) -> Any:
    """
    缓存导入模块

    :param module_name:
    :return:
    """
    return importlib.import_module(module_name)


def dynamic_import(module_path: str) -> Any:
    """
    动态导入

    :param module_path:
    :return:
    """
    module_name, class_or_func = module_parse(module_path)
    module = import_module_cached(module_name)
    ins = getattr(module, class_or_func)
    return ins
