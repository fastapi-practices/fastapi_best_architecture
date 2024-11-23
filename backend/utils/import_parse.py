#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib

from typing import Any


def parse_module_str(module_path: str) -> tuple:
    """
    Parse a module string into a Python module and class/function.

    :param module_path:
    :return:
    """
    module_name, class_or_func = module_path.rsplit('.', 1)
    return module_name, class_or_func


def dynamic_import(module_path: str) -> Any:
    """
    动态导入

    :param module_path:
    :return:
    """
    module_name, object_name = parse_module_str(module_path)
    module = importlib.import_module(module_name)
    class_or_func = getattr(module, object_name)
    return class_or_func
