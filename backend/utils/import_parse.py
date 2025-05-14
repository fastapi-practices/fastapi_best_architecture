#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib

from functools import lru_cache
from typing import Any, Type, TypeVar

from backend.common.exception import errors
from backend.common.log import log

T = TypeVar('T')


@lru_cache(maxsize=512)
def import_module_cached(module_path: str) -> Any:
    """
    Cache Import Module

    :param modeule_path: modular path
    :return:
    """
    return importlib.import_module(module_path)


def dynamic_import_data_model(module_path: str) -> Type[T]:
    """
    Dynamic Import Data Model

    :param modeule_path: module path, formatted as 'module_path.class_name '
    :return:
    """
    try:
        module_path, class_name = module_path.rsplit('.', 1)
        module = import_module_cached(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        log.error(f'dynamic import data model failed: {e}')
        raise errors.ServerError(msg='Data model column dynamical resolution failed. Please contact the system supermanager')
