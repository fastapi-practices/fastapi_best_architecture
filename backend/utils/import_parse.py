#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib
import inspect

from functools import lru_cache
from typing import Any, Type, TypeVar

from backend.common.exception import errors
from backend.common.log import log

T = TypeVar('T')


@lru_cache(maxsize=512)
def import_module_cached(module_path: str) -> Any:
    """
    缓存导入模块

    :param module_path: 模块路径
    :return:
    """
    return importlib.import_module(module_path)


def dynamic_import_data_model(module_path: str) -> Type[T]:
    """
    动态导入数据模型

    :param module_path: 模块路径，格式为 'module_path.class_name'
    :return:
    """
    try:
        module_path, class_name = module_path.rsplit('.', 1)
        module = import_module_cached(module_path)
        return getattr(module, class_name)
    except Exception as e:
        log.error(f'动态导入数据模型失败：{e}')
        raise errors.ServerError(msg='数据模型列动态解析失败，请联系系统超级管理员')


def get_model_object(module_path: str) -> type | None:
    """
    获取模型对象

    :param module_path: 模块路径
    :return:
    """
    try:
        module = import_module_cached(module_path)
    except ModuleNotFoundError:
        log.warning(f'模块 {module_path} 中不包含模型对象')
        return None
    except Exception as e:
        raise RuntimeError(f'获取模块 {module_path} 模型对象失败：{e}')

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            return obj

    return None
