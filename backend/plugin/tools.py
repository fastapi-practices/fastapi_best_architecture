#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import os
import subprocess
import sys
import warnings

from typing import Any

import rtoml

from fastapi import APIRouter
from starlette.concurrency import run_in_threadpool

from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR
from backend.utils.import_parse import import_module_cached


class PluginInjectError(Exception):
    """插件注入错误"""


def get_plugins() -> list[str]:
    """获取插件列表"""
    plugin_packages = []

    # 遍历插件目录
    for item in os.listdir(PLUGIN_DIR):
        item_path = os.path.join(PLUGIN_DIR, item)

        # 检查是否为目录且包含 __init__.py 文件
        if os.path.isdir(item_path) and '__init__.py' in os.listdir(item_path):
            plugin_packages.append(item)

    return plugin_packages


def get_plugin_models() -> list[type]:
    """获取插件所有模型类"""
    classes = []

    # 获取所有插件
    plugins = get_plugins()

    for plugin in plugins:
        # 导入插件的模型模块
        module_path = f'backend.plugin.{plugin}.model'
        module = import_module_cached(module_path)

        # 获取模块中的所有类
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                classes.append(obj)

    return classes


def load_plugin_config(plugin: str) -> dict[str, Any]:
    """
    加载插件配置

    :param plugin: 插件名称
    :return:
    """
    toml_path = os.path.join(PLUGIN_DIR, plugin, 'plugin.toml')
    if not os.path.exists(toml_path):
        raise PluginInjectError(f'插件 {plugin} 缺少 plugin.toml 配置文件，请检查插件是否合法')

    with open(toml_path, 'r', encoding='utf-8') as f:
        return rtoml.load(f)


def inject_extra_router(plugin: str, data: dict[str, Any]) -> None:
    """
    扩展级插件路由注入

    :param plugin: 插件名称
    :param data: 插件配置数据
    :return:
    """
    app_include = data.get('app', {}).get('include', '')
    if not app_include:
        raise PluginInjectError(f'扩展级插件 {plugin} 配置文件存在错误，请检查')

    plugin_api_path = os.path.join(PLUGIN_DIR, plugin, 'api')
    if not os.path.exists(plugin_api_path):
        raise PluginInjectError(f'插件 {plugin} 缺少 api 目录，请检查插件文件是否完整')

    for root, _, api_files in os.walk(plugin_api_path):
        for file in api_files:
            if not (file.endswith('.py') and file != '__init__.py'):
                continue

            # 解析插件路由配置
            file_config = data.get('api', {}).get(f'{file[:-3]}', {})
            prefix = file_config.get('prefix', '')
            tags = file_config.get('tags', [])

            # 获取插件路由模块
            file_path = os.path.join(root, file)
            path_to_module_str = os.path.relpath(file_path, PLUGIN_DIR).replace(os.sep, '.')[:-3]
            module_path = f'backend.plugin.{path_to_module_str}'

            try:
                module = import_module_cached(module_path)
                plugin_router = getattr(module, 'router', None)
                if not plugin_router:
                    warnings.warn(
                        f'扩展级插件 {plugin} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整',
                        FutureWarning,
                    )
                    continue

                # 获取目标 app 路由
                relative_path = os.path.relpath(root, plugin_api_path)
                target_module_path = f'backend.app.{app_include}.api.{relative_path.replace(os.sep, ".")}'
                target_module = import_module_cached(target_module_path)
                target_router = getattr(target_module, 'router', None)

                if not target_router or not isinstance(target_router, APIRouter):
                    raise PluginInjectError(
                        f'扩展级插件 {plugin} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整'
                    )

                # 将插件路由注入到目标路由中
                target_router.include_router(
                    router=plugin_router,
                    prefix=prefix,
                    tags=[tags] if tags else [],
                )
            except Exception as e:
                raise PluginInjectError(f'扩展级插件 {plugin} 路由注入失败：{str(e)}') from e


def inject_app_router(plugin: str, data: dict[str, Any]) -> None:
    """
    应用级插件路由注入

    :param plugin: 插件名称
    :param data: 插件配置数据
    :return:
    """
    module_path = f'backend.plugin.{plugin}.api.router'
    try:
        module = import_module_cached(module_path)
        routers = data.get('app', {}).get('router', [])
        if not routers or not isinstance(routers, list):
            raise PluginInjectError(f'应用级插件 {plugin} 配置文件存在错误，请检查')

        # 获取目标路由
        target_module = import_module_cached('backend.app.router')
        target_router = getattr(target_module, 'router')

        for router in routers:
            plugin_router = getattr(module, router, None)
            if not plugin_router or not isinstance(plugin_router, APIRouter):
                raise PluginInjectError(
                    f'应用级插件 {plugin} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整'
                )

            # 将插件路由注入到目标路由中
            target_router.include_router(plugin_router)
    except Exception as e:
        raise PluginInjectError(f'应用级插件 {plugin} 路由注入失败：{str(e)}') from e


def plugin_router_inject() -> None:
    """插件路由注入"""
    for plugin in get_plugins():
        data = load_plugin_config(plugin)
        # 基于插件 plugin.toml 配置文件，判断插件类型
        if data.get('api'):
            inject_extra_router(plugin, data)
        else:
            inject_app_router(plugin, data)


def _install_plugin_requirements(plugin: str, requirements_file: str) -> None:
    """
    安装单个插件的依赖

    :param plugin: 插件名称
    :param requirements_file: 依赖文件路径
    :return:
    """
    try:
        ensurepip_install = [sys.executable, '-m', 'ensurepip', '--upgrade']
        pip_install = [sys.executable, '-m', 'pip', 'install', '-r', requirements_file]
        if settings.PLUGIN_PIP_CHINA:
            pip_install.extend(['-i', settings.PLUGIN_PIP_INDEX_URL])
        subprocess.check_call(ensurepip_install)
        subprocess.check_call(pip_install)
    except subprocess.CalledProcessError as e:
        raise PluginInjectError(f'插件 {plugin} 依赖安装失败：{e.stderr}') from e


def install_requirements() -> None:
    """安装插件依赖"""
    for plugin in get_plugins():
        requirements_file = os.path.join(PLUGIN_DIR, plugin, 'requirements.txt')
        if os.path.exists(requirements_file):
            _install_plugin_requirements(plugin, requirements_file)


async def install_requirements_async() -> None:
    """
    异步安装插件依赖

    由于 Windows 平台限制，无法实现完美的全异步方案，详情：
    https://stackoverflow.com/questions/44633458/why-am-i-getting-notimplementederror-with-async-and-await-on-windows
    """
    await run_in_threadpool(install_requirements)
