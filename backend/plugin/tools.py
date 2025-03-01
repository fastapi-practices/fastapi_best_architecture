#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import inspect
import os
import subprocess
import sys
import warnings

from asyncio import subprocess as async_subprocess

import rtoml

from fastapi import APIRouter

from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR
from backend.utils.import_parse import import_module_cached


class PluginInjectError(Exception):
    pass


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


def plugin_router_inject() -> None:
    """
    插件路由注入

    :return:
    """
    plugins = get_plugins()
    for plugin in plugins:
        toml_path = os.path.join(PLUGIN_DIR, plugin, 'plugin.toml')
        if not os.path.exists(toml_path):
            raise PluginInjectError(f'插件 {plugin} 缺少 plugin.toml 配置文件，请检查插件是否合法')

        # 获取 plugin.toml 配置
        with open(toml_path, 'r', encoding='utf-8') as f:
            data = rtoml.load(f)
        api = data.get('api', {})

        # 非独立 app
        if api:
            app_include = data.get('app', {}).get('include', '')
            if not app_include:
                raise PluginInjectError(f'非独立 app 插件 {plugin} 配置文件存在错误，请检查')

            # 插件中 API 路由文件的路径
            plugin_api_path = os.path.join(PLUGIN_DIR, plugin, 'api')
            if not os.path.exists(plugin_api_path):
                raise PluginInjectError(f'插件 {plugin} 缺少 api 目录，请检查插件文件是否完整')

            # 将插件路由注入到对应模块的路由中
            for root, _, api_files in os.walk(plugin_api_path):
                for file in api_files:
                    if file.endswith('.py') and file != '__init__.py':
                        # 解析插件路由配置
                        prefix = data.get('api', {}).get(f'{file[:-3]}', {}).get('prefix', '')
                        tags = data.get('api', {}).get(f'{file[:-3]}', {}).get('tags', [])

                        # 获取插件路由模块
                        file_path = os.path.join(root, file)
                        path_to_module_str = os.path.relpath(file_path, PLUGIN_DIR).replace(os.sep, '.')[:-3]
                        module_path = f'backend.plugin.{path_to_module_str}'
                        try:
                            module = import_module_cached(module_path)
                        except PluginInjectError as e:
                            raise PluginInjectError(f'导入非独立 app 插件 {plugin} 模块 {module_path} 失败：{e}') from e
                        plugin_router = getattr(module, 'router', None)
                        if not plugin_router:
                            warnings.warn(
                                f'非独立 app 插件 {plugin} 模块 {module_path} 中没有有效的 router，'
                                '请检查插件文件是否完整',
                                FutureWarning,
                            )
                            continue

                        # 获取源程序路由模块
                        relative_path = os.path.relpath(root, plugin_api_path)
                        target_module_path = f'backend.app.{app_include}.api.{relative_path.replace(os.sep, ".")}'
                        try:
                            target_module = import_module_cached(target_module_path)
                        except PluginInjectError as e:
                            raise PluginInjectError(f'导入源程序模块 {target_module_path} 失败：{e}') from e
                        target_router = getattr(target_module, 'router', None)
                        if not target_router or not isinstance(target_router, APIRouter):
                            raise PluginInjectError(
                                f'非独立 app 插件 {plugin} 模块 {module_path} 中没有有效的 router，'
                                '请检查插件文件是否完整'
                            )

                        # 将插件路由注入到目标 router 中
                        target_router.include_router(
                            router=plugin_router,
                            prefix=prefix,
                            tags=[tags] if tags else [],
                        )
        # 独立 app
        else:
            # 将插件中的路由直接注入到总路由中
            module_path = f'backend.plugin.{plugin}.api.router'
            try:
                module = import_module_cached(module_path)
            except PluginInjectError as e:
                raise PluginInjectError(f'导入独立 app 插件 {plugin} 模块 {module_path} 失败：{e}') from e
            routers = data.get('app', {}).get('router', [])
            if not routers or not isinstance(routers, list):
                raise PluginInjectError(f'独立 app 插件 {plugin} 配置文件存在错误，请检查')
            for router in routers:
                plugin_router = getattr(module, router, None)
                if not plugin_router or not isinstance(plugin_router, APIRouter):
                    raise PluginInjectError(
                        f'独立 app 插件 {plugin} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整'
                    )
                target_module_path = 'backend.app.router'
                target_module = import_module_cached(target_module_path)
                target_router = getattr(target_module, 'router')

                # 将插件路由注入到目标 router 中
                target_router.include_router(plugin_router)


def install_requirements() -> None:
    """安装插件依赖"""
    plugins = get_plugins()
    for plugin in plugins:
        requirements_file = os.path.join(PLUGIN_DIR, plugin, 'requirements.txt')
        if not os.path.exists(requirements_file):
            continue
        else:
            try:
                subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'])
                pip_requirements = [sys.executable, '-m', 'pip', 'install', '-r', requirements_file]
                if settings.PLUGIN_PIP_CHINA:
                    pip_requirements.extend(['-i', settings.PLUGIN_PIP_INDEX_URL])
                subprocess.check_call(pip_requirements)
            except subprocess.CalledProcessError as e:
                raise PluginInjectError(f'插件 {plugin} 依赖安装失败：{e}') from e


async def install_requirements_async(wait: bool = True) -> None:
    """
    异步安装插件依赖

    :param wait: 是否等待结果并校验，开启将造成 IO 阻塞
    :return:
    """
    plugins = get_plugins()
    for plugin in plugins:
        requirements_file = os.path.join(PLUGIN_DIR, plugin, 'requirements.txt')
        if not os.path.exists(requirements_file):
            continue
        else:
            ensurepip_process = await async_subprocess.create_subprocess_exec(
                sys.executable,
                '-m',
                'ensurepip',
                '--upgrade',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            if wait:
                _, ensurepip_stderr = await ensurepip_process.communicate()
                if ensurepip_process.returncode != 0:
                    raise PluginInjectError(f'ensurepip 安装失败：{ensurepip_stderr}')
            pip_requirements = [sys.executable, '-m', 'pip', 'install', '-r', requirements_file]
            if settings.PLUGIN_PIP_CHINA:
                pip_requirements.extend(['-i', settings.PLUGIN_PIP_INDEX_URL])
            pip_process = await async_subprocess.create_subprocess_exec(
                *pip_requirements,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            if wait:
                _, pip_stderr = await pip_process.communicate()
                if pip_process.returncode != 0:
                    raise PluginInjectError(f'插件 {plugin} 依赖包安装失败：{pip_stderr}')
