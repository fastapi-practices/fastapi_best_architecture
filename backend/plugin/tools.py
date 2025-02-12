#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import os

import rtoml

from fastapi import FastAPI

from backend.core.path_conf import PLUGIN_DIR
from backend.utils.import_parse import import_module_cached


def get_plugins() -> list[str]:
    """获取插件"""
    plugin_packages = []

    for item in os.listdir(PLUGIN_DIR):
        item_path = os.path.join(PLUGIN_DIR, item)

        if os.path.isdir(item_path):
            if '__init__.py' in os.listdir(item_path):
                plugin_packages.append(item)

    return plugin_packages


def get_plugin_models() -> list:
    """获取插件所有模型类"""
    classes = []
    plugins = get_plugins()
    for plugin in plugins:
        module_path = f'backend.plugin.{plugin}.model'
        module = import_module_cached(module_path)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                classes.append(obj)
    return classes


def register_plugin_router(app: FastAPI):
    """
    插件路由注入

    :param app:
    :return:
    """
    plugins = get_plugins()
    for plugin in plugins:
        toml_path = os.path.join(PLUGIN_DIR, plugin, 'plugin.toml')
        if not os.path.exists(toml_path):
            raise FileNotFoundError('插件缺少 plugin.toml 配置文件')

        toml_data = rtoml.load(toml_path)
        app_name = toml_data.get('app', '')
        api_module = toml_data.get('api', {}).get('module', '')
        prefix = toml_data.get('api', {}).get('prefix', '')

        if app_name:
            if '.' in api_module:
                module_path = f'backend.app.{app_name}.api.{api_module}'
            else:
                module_path = f'backend.app.{app_name}.api'
        else:
            module_path = 'backend.app'

        try:
            module = import_module_cached(module_path)
        except ImportError as e:
            raise ImportError(f'导入模块 {module_path} 失败：{e}') from e
        else:
            if app_name and '.' in api_module:
                # 从 backend.app.xxx.api.vx.xxx.__init__.py 文件中获取路由
                router = getattr(module, 'router', None)
            else:
                if 'api' in module_path:
                    # 从 backend.app.xxx.api 下的 router.py 文件中获取路由
                    router = getattr(module, api_module.split('.')[0], None)
                else:
                    # 从 backend.app 下的 router.py 文件中获取路由
                    router = getattr(module, 'router', None)

            if not router:
                raise ImportError(f'模块 {module_path} 中不存在路由')

            if app_name:
                app.include_router(router, prefix=f'/{prefix}')
            else:
                app.include_router(router)
