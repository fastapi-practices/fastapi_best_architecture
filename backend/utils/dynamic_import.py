import importlib
import inspect
import os.path

from functools import lru_cache
from typing import Any, TypeVar

import sqlalchemy as sa

from backend.common.exception import errors
from backend.common.log import log

T = TypeVar('T')


@lru_cache(maxsize=128)
def import_module_cached(module_path: str) -> Any:
    """
    缓存导入模块

    :param module_path: 模块路径
    :return:
    """
    return importlib.import_module(module_path)


def dynamic_import_data_model(module_path: str) -> type[T]:
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


def get_model_objects(module_path: str) -> list[object] | None:
    """
    获取模型对象

    :param module_path: 模块路径
    :return:
    """
    try:
        module = import_module_cached(module_path)
    except ModuleNotFoundError:
        return None
    except Exception as e:
        raise e from None

    classes = []

    for _name, obj in inspect.getmembers(module):
        if (inspect.isclass(obj) and module_path in obj.__module__) or (
            isinstance(obj, sa.Table) and obj.metadata is not None
        ):
            classes.append(obj)

    return classes


def get_app_models() -> list[object]:
    """获取 app 所有模型类"""
    from backend.core.path_conf import BASE_PATH

    app_path = BASE_PATH / 'app'
    list_dirs = os.listdir(app_path)

    apps = [d for d in list_dirs if os.path.isdir(os.path.join(app_path, d)) and d != '__pycache__']

    objs = []
    for app in apps:
        module_path = f'backend.app.{app}.model'
        model_objs = get_model_objects(module_path)
        if model_objs:
            objs.extend(model_objs)

    return objs


@lru_cache(256)
def get_all_models() -> tuple[object, ...]:
    """获取所有模型类"""
    from backend.plugin.core import get_plugin_models

    return tuple(get_app_models() + get_plugin_models())
