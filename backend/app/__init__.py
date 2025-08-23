#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

from backend.core.path_conf import BASE_PATH
from backend.utils.import_parse import get_model_object


def get_app_models() -> list[type]:
    """获取 app 所有模型类"""
    app_path = os.path.join(BASE_PATH, 'app')
    list_dirs = os.listdir(app_path)

    apps = []

    for d in list_dirs:
        if os.path.isdir(os.path.join(app_path, d)) and d != '__pycache__':
            apps.append(d)

    objs = []

    for app in apps:
        module_path = f'backend.app.{app}.model'
        obj = get_model_object(module_path)
        if obj:
            objs.append(obj)

    return objs


# import all app models for auto create db tables
for cls in get_app_models():
    class_name = cls.__name__
    if class_name not in globals():
        globals()[class_name] = cls
