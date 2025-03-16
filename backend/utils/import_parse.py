#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib

from functools import lru_cache
from typing import Any

from backend.common.exception import errors
from backend.common.log import log


@lru_cache(maxsize=512)
def import_module_cached(module_path: str) -> Any:
    """
    缓存导入模块

    :param module_path:
    :return:
    """
    return importlib.import_module(module_path)


def dynamic_import_data_model(module_path: str) -> Any:
    """
    动态导入数据模型

    :param module_path:
    :return:
    """
    module_path, class_or_func = module_path.rsplit('.', 1)

    try:
        module = import_module_cached(module_path)
        ins = getattr(module, class_or_func)
    except (ImportError, AttributeError) as e:
        log.error(e)
        raise errors.ServerError(msg='数据模型列动态解析失败，请联系系统超级管理员')
    return ins
