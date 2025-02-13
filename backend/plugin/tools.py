#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib
import inspect
import os
import warnings

import rtoml

from fastapi import APIRouter

from backend.core.path_conf import PLUGIN_DIR


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
        module = importlib.import_module(module_path)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                classes.append(obj)
    return classes


def plugin_router_inject(router: APIRouter) -> APIRouter:
    """
    插件路由注入

    :param router: 源总路由器
    :return: 注入插件路由后的总路由器
    """
    plugins = get_plugins()
    for plugin in plugins:
        toml_path = os.path.join(PLUGIN_DIR, plugin, 'plugin.toml')
        if not os.path.exists(toml_path):
            raise FileNotFoundError(f'插件 {plugin} 缺少 plugin.toml 配置文件，请检查插件是否合法')

        # 解析 plugin.toml
        with open(toml_path, 'r', encoding='utf-8') as f:
            data = rtoml.load(f)
        app_name = data.get('app', '')
        prefix = data.get('api', {}).get('prefix', '')
        tags = data.get('api', {}).get('tags', [])

        # 插件中 API 路由文件的路径
        plugin_api_path = os.path.join(PLUGIN_DIR, plugin, 'api')
        if not os.path.exists(plugin_api_path):
            raise FileNotFoundError(f'插件 {plugin} 缺少 api 目录，请检查插件文件是否完整')

        # 路由注入
        if app_name:
            # 非独立应用：将插件中的路由注入到源程序对应模块的路由中
            for root, _, api_files in os.walk(plugin_api_path):
                for file in api_files:
                    if file.endswith('.py') and file != '__init__.py':
                        api_files_path = os.path.join(root, file)

                        # 获取插件路由模块
                        path_to_module_str = os.path.relpath(api_files_path, PLUGIN_DIR).replace(os.sep, '.')[:-3]
                        module_path = f'backend.plugin.{path_to_module_str}'
                        try:
                            module = importlib.import_module(module_path)
                        except ImportError as e:
                            raise ImportError(f'导入模块 {module_path} 失败：{e}') from e
                        plugin_router = getattr(module, 'router', None)
                        if not plugin_router:
                            warnings.warn(
                                f'目标模块 {module_path} 中没有有效的 router，请检查插件文件是否完整',
                                FutureWarning,
                            )
                            continue

                        # 获取源程序路由模块
                        relative_path = os.path.relpath(root, plugin_api_path)
                        target_module_path = f'backend.app.{app_name}.api.{relative_path.replace(os.sep, ".")}'
                        try:
                            target_module = importlib.import_module(target_module_path)
                        except ImportError as e:
                            raise ImportError(f'导入目标模块 {target_module_path} 失败：{e}') from e
                        target_router = getattr(target_module, 'router', None)
                        if not target_router or not isinstance(target_router, APIRouter):
                            raise AttributeError(f'目标模块 {module_path} 中没有有效的 router，请检查插件文件是否完整')

                        # 将插件路由注入到目标 router 中
                        target_router.include_router(
                            router=plugin_router,
                            prefix=prefix,
                            tags=tags if type(tags) is list else [tags],
                        )
        else:
            # 独立应用：将插件中的路由直接注入到 app 中
            module_path = f'backend.plugin.{plugin}.api.router'
            try:
                target_module = importlib.import_module(module_path)
            except ImportError as e:
                raise ImportError(f'导入目标模块 {module_path} 失败：{e}') from e
            target_router = getattr(target_module, 'router', None)
            if not target_router or not isinstance(target_router, APIRouter):
                raise AttributeError(f'目标模块 {module_path} 中没有有效的 router，请检查插件文件是否完整')
            router.include_router(target_router)

    return router
