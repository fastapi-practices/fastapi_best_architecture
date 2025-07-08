#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import os.path

from backend.common.log import log
from backend.core.path_conf import BASE_PATH
from backend.utils.import_parse import import_module_cached


def get_app_models():
    """获取 app 所有模型类"""
    app_path = os.path.join(BASE_PATH, 'app')
    list_dirs = os.listdir(app_path)

    apps = []

    for d in list_dirs:
        if os.path.isdir(os.path.join(app_path, d)) and d != '__pycache__':
            apps.append(d)

    classes = []

    for app in apps:
        try:
            module_path = f'backend.app.{app}.model'
            module = import_module_cached(module_path)
        except Exception as e:
            log.warning(f'应用 {app} 中不包含 model 相关配置: {e}')
            continue

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                classes.append(obj)

    return classes


# import all app models for auto create db tables
for cls in get_app_models():
    class_name = cls.__name__
    if class_name not in globals():
        globals()[class_name] = cls
