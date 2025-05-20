#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import json
import os
import subprocess
import sys
import warnings

from functools import lru_cache
from typing import Any

import rtoml

from fastapi import APIRouter, Depends, Request
from starlette.concurrency import run_in_threadpool

from backend.common.enums import StatusType
from backend.common.exception.errors import ForbiddenError
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR
from backend.database.redis import RedisCli, redis_client
from backend.plugin.errors import PluginConfigError, PluginInjectError
from backend.utils._asyncio import run_await
from backend.utils.import_parse import import_module_cached


@lru_cache
def get_plugins() -> list[str]:
    """获取插件列表"""
    plugin_packages = []

    # 遍历插件目录
    for item in os.listdir(PLUGIN_DIR):
        if item.endswith('.py') or item.endswith('backup') or item == '__pycache__':
            continue

        item_path = os.path.join(PLUGIN_DIR, item)

        # 检查是否为目录且包含 __init__.py 文件
        if os.path.isdir(item_path) and '__init__.py' in os.listdir(item_path):
            plugin_packages.append(item)

    return plugin_packages


def get_plugin_models() -> list[type]:
    """获取插件所有模型类"""
    classes = []

    for plugin in get_plugins():
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


def parse_plugin_config() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """解析插件配置"""

    extra_plugins = []
    app_plugins = []

    plugins = get_plugins()

    # 使用独立单例，避免与主线程冲突
    current_redis_client = RedisCli()
    run_await(current_redis_client.open)()

    run_await(current_redis_client.delete_prefix)(f'{settings.PLUGIN_REDIS_PREFIX}:info', exclude=plugins)
    plugin_status = run_await(current_redis_client.hgetall)(f'{settings.PLUGIN_REDIS_PREFIX}:status')
    if not plugin_status:
        plugin_status = {}

    for plugin in plugins:
        data = load_plugin_config(plugin)

        plugin_info = data.get('plugin')
        if not plugin_info:
            raise PluginConfigError(f'插件 {plugin} 配置文件缺少 plugin 配置')

        required_fields = ['summary', 'version', 'description', 'author']
        missing_fields = [field for field in required_fields if field not in plugin_info]
        if missing_fields:
            raise PluginConfigError(f'插件 {plugin} 配置文件缺少必要字段: {", ".join(missing_fields)}')

        if data.get('api'):
            if not data.get('app', {}).get('include'):
                raise PluginConfigError(f'扩展级插件 {plugin} 配置文件缺少 app.include 配置')
            extra_plugins.append(data)
        else:
            if not data.get('app', {}).get('router'):
                raise PluginConfigError(f'应用级插件 {plugin} 配置文件缺少 app.router 配置')
            app_plugins.append(data)

        # 补充插件信息
        data['plugin']['enable'] = plugin_status.setdefault(plugin, str(StatusType.enable.value))
        data['plugin']['name'] = plugin

        # 缓存插件信息
        run_await(current_redis_client.set)(
            f'{settings.PLUGIN_REDIS_PREFIX}:info:{plugin}', json.dumps(data, ensure_ascii=False)
        )

    # 缓存插件状态
    run_await(current_redis_client.hset)(f'{settings.PLUGIN_REDIS_PREFIX}:status', mapping=plugin_status)
    run_await(current_redis_client.delete)(f'{settings.PLUGIN_REDIS_PREFIX}:changed')

    return extra_plugins, app_plugins


def inject_extra_router(plugin: dict[str, Any]) -> None:
    """
    扩展级插件路由注入

    :param plugin: 插件名称
    :return:
    """
    plugin_name: str = plugin['plugin']['name']
    plugin_api_path = os.path.join(PLUGIN_DIR, plugin_name, 'api')
    if not os.path.exists(plugin_api_path):
        raise PluginConfigError(f'插件 {plugin} 缺少 api 目录，请检查插件文件是否完整')

    for root, _, api_files in os.walk(plugin_api_path):
        for file in api_files:
            if not (file.endswith('.py') and file != '__init__.py'):
                continue

            # 解析插件路由配置
            file_config = plugin.get('api', {}).get(f'{file[:-3]}', {})
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
                        f'扩展级插件 {plugin_name} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整',
                        FutureWarning,
                    )
                    continue

                # 获取目标 app 路由
                relative_path = os.path.relpath(root, plugin_api_path)
                target_module_path = (
                    f'backend.app.{plugin.get("app", {}).get("include")}.api.{relative_path.replace(os.sep, ".")}'
                )
                target_module = import_module_cached(target_module_path)
                target_router = getattr(target_module, 'router', None)

                if not target_router or not isinstance(target_router, APIRouter):
                    raise PluginInjectError(
                        f'扩展级插件 {plugin_name} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整'
                    )

                # 将插件路由注入到目标路由中
                target_router.include_router(
                    router=plugin_router,
                    prefix=prefix,
                    tags=[tags] if tags else [],
                    dependencies=[Depends(PluginStatusChecker(plugin_name))],
                )
            except Exception as e:
                raise PluginInjectError(f'扩展级插件 {plugin_name} 路由注入失败：{str(e)}') from e


def inject_app_router(plugin: dict[str, Any], target_router: APIRouter) -> None:
    """
    应用级插件路由注入

    :param plugin: 插件名称
    :param target_router: FastAPI 路由器
    :return:
    """
    plugin_name: str = plugin['plugin']['name']
    module_path = f'backend.plugin.{plugin_name}.api.router'
    try:
        module = import_module_cached(module_path)
        routers = plugin.get('app', {}).get('router')
        if not routers or not isinstance(routers, list):
            raise PluginConfigError(f'应用级插件 {plugin_name} 配置文件存在错误，请检查')

        for router in routers:
            plugin_router = getattr(module, router, None)
            if not plugin_router or not isinstance(plugin_router, APIRouter):
                raise PluginInjectError(
                    f'应用级插件 {plugin_name} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整'
                )

            # 将插件路由注入到目标路由中
            target_router.include_router(plugin_router, dependencies=[Depends(PluginStatusChecker(plugin_name))])
    except Exception as e:
        raise PluginInjectError(f'应用级插件 {plugin_name} 路由注入失败：{str(e)}') from e


def build_final_router() -> APIRouter:
    """构建最终路由"""
    extra_plugins, app_plugins = parse_plugin_config()

    for plugin in extra_plugins:
        inject_extra_router(plugin)

    # 主路由，必须在插件路由注入后导入
    from backend.app.router import router as main_router

    for plugin in app_plugins:
        inject_app_router(plugin, main_router)

    return main_router


def install_requirements(plugin: str) -> None:
    """
    安装插件依赖

    :param plugin: 指定插件名，否则检查所有插件
    :return:
    """
    plugins = [plugin] if plugin else get_plugins()

    for plugin in plugins:
        requirements_file = os.path.join(PLUGIN_DIR, plugin, 'requirements.txt')
        if os.path.exists(requirements_file):
            try:
                ensurepip_install = [sys.executable, '-m', 'ensurepip', '--upgrade']
                pip_install = [sys.executable, '-m', 'pip', 'install', '-r', requirements_file]
                if settings.PLUGIN_PIP_CHINA:
                    pip_install.extend(['-i', settings.PLUGIN_PIP_INDEX_URL])
                subprocess.check_call(ensurepip_install)
                subprocess.check_call(pip_install)
            except subprocess.CalledProcessError as e:
                raise PluginInjectError(f'插件 {plugin} 依赖安装失败：{e.stderr}') from e


def uninstall_requirements(plugin: str) -> None:
    """
    卸载插件依赖

    :param plugin: 插件名称
    :return:
    """
    requirements_file = os.path.join(PLUGIN_DIR, plugin, 'requirements.txt')
    if os.path.exists(requirements_file):
        try:
            pip_uninstall = [sys.executable, '-m', 'pip', 'uninstall', '-r', requirements_file, '-y']
            subprocess.check_call(pip_uninstall)
        except subprocess.CalledProcessError as e:
            raise PluginInjectError(f'插件 {plugin} 依赖卸载失败：{e.stderr}') from e


async def install_requirements_async(plugin: str | None = None) -> None:
    """
    异步安装插件依赖

    由于 Windows 平台限制，无法实现完美的全异步方案，详情：
    https://stackoverflow.com/questions/44633458/why-am-i-getting-notimplementederror-with-async-and-await-on-windows
    """
    await run_in_threadpool(install_requirements, plugin)


async def uninstall_requirements_async(plugin: str) -> None:
    """
    异步卸载插件依赖

    :param plugin: 插件名称
    :return:
    """
    await run_in_threadpool(uninstall_requirements, plugin)


class PluginStatusChecker:
    """插件状态检查器"""

    def __init__(self, plugin: str) -> None:
        """
        初始化插件状态检查器

        :param plugin: 插件名称
        :return:
        """
        self.plugin = plugin

    async def __call__(self, request: Request) -> None:
        """
        验证插件状态

        :param request: FastAPI 请求对象
        :return:
        """
        plugin_status = await redis_client.hgetall(f'{settings.PLUGIN_REDIS_PREFIX}:status')
        if not plugin_status:
            log.error('插件状态未初始化或丢失，需重启服务自动修复')
            raise PluginInjectError('插件状态未初始化或丢失，请联系系统管理员')

        if self.plugin not in plugin_status:
            log.error(f'插件 {self.plugin} 状态未初始化或丢失，需重启服务自动修复')
            raise PluginInjectError(f'插件 {self.plugin} 状态未初始化或丢失，请联系系统管理员')
        if not int(plugin_status.get(self.plugin)):
            raise ForbiddenError(msg=f'插件 {self.plugin} 未启用，请联系系统管理员')
