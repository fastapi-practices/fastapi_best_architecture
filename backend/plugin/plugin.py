#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import os

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


def get_plugin_models():
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


if __name__ == '__main__':
    print(get_plugins())
    print(get_plugin_models())
