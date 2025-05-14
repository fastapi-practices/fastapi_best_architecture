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
    """Plugin In error"""


def get_plugins() -> list[str]:
    """Fetch Plugin List"""
    plugin_packages = []

    # Through Plugin Directory
    for item in os.listdir(PLUGIN_DIR):
        item_path = os.path.join(PLUGIN_DIR, item)

        # check if it is a directory and contains ___init__.py files
        if os.path.isdir(item_path) and '__init__.py' in os.listdir(item_path):
            plugin_packages.append(item)

    return plugin_packages


def get_plugin_models() -> list[type]:
    """Fetch plugins for all model categories"""
    classes = []

    # Get All Plugins
    plugins = get_plugins()

    for plugin in plugins:
        # Model module for importing plugins
        module_path = f'backend.plugin.{plugin}.model'
        module = import_module_cached(module_path)

        # Get all classes in the module
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                classes.append(obj)

    return classes


def load_plugin_config(plugin: str) -> dict[str, Any]:
    """
    Load Plugin Configuration

    :param plugin: plugin name
    :return:
    """
    toml_path = os.path.join(PLUGIN_DIR, plugin, 'plugin.toml')
    if not os.path.exists(toml_path):
        raise PluginInjectError(
            f'plugin {plugin} missing plugin.toml profile, check the plugin \'s validity')

    with open(toml_path, 'r', encoding='utf-8') as f:
        return rtoml.load(f)


def inject_extra_router(plugin: str, data: dict[str, Any]) -> None:
    """
    Extension Plugin Path Injection

    :param plugin: plugin name
    :param data: plugin configuration data
    :return:
    """
    app_include = data.get('app', {}).get('include', '')
    if not app_include:
        raise PluginInjectError(
            f'extension plugin {plugin} profile error, check')

    plugin_api_path = os.path.join(PLUGIN_DIR, plugin, 'api')
    if not os.path.exists(plugin_api_path):
        raise PluginInjectError(
            f'plugin {plugin} missing api directory, check if the plugin file is complete')

    for root, _, api_files in os.walk(plugin_api_path):
        for file in api_files:
            if not (file.endswith('.py') and file != '__init__.py'):
                continue

            # Parsing Plugin Route Configuration
            file_config = data.get('api', {}).get(f'{file[:-3]}', {})
            prefix = file_config.get('prefix', '')
            tags = file_config.get('tags', [])

            # Get Plugin Route Module
            file_path = os.path.join(root, file)
            path_to_module_str = os.path.relpath(
                file_path, PLUGIN_DIR).replace(os.sep, '.')[:-3]
            module_path = f'backend.plugin.{path_to_module_str}'

            try:
                module = import_module_cached(module_path)
                plugin_router = getattr(module, 'router', None)
                if not plugin_router:
                    warnings.warn(
                        f'the extension plugin {plugin} module {module_path} does not have a valid router. check if the plugin file is complete',
                        FutureWarning,
                    )
                    continue

                # get target app route
                relative_path = os.path.relpath(root, plugin_api_path)
                target_module_path = f'backend.app.{app_include}.api.{relative_path.replace(os.sep, ".")}'
                target_module = import_module_cached(target_module_path)
                target_router = getattr(target_module, 'router', None)

                if not target_router or not isinstance(target_router, APIRouter):
                    raise PluginInjectError(
                        f'the extension plugin {plugin} module {module_path} does not have a valid router. check if the plugin file is complete'
                    )

                # Plugin routed into target route
                target_router.include_router(
                    router=plugin_router,
                    prefix=prefix,
                    tags=[tags] if tags else [],
                )
            except Exception as e:
                raise PluginInjectError(
                    f'extension plugin {plugin} route injection failed:{str(e)}') from e


def inject_app_router(plugin: str, data: dict[str, Any], target_router: APIRouter) -> None:
    """
    Application-level plugin route infusion

    :param plugin: plugin name
    :param data: plugin configuration data
    :param target_router: FastAPI router
    :return:
    """
    module_path = f'backend.plugin.{plugin}.api.router'
    try:
        module = import_module_cached(module_path)
        routers = data.get('app', {}).get('router', [])
        if not routers or not isinstance(routers, list):
            raise PluginInjectError(
                f'error in application level plugin {plugin} configuration file, check')

        for router in routers:
            plugin_router = getattr(module, router, None)
            if not plugin_router or not isinstance(plugin_router, APIRouter):
                raise PluginInjectError(
                    f'the application level plugin {plugin} module {module_path} does not have a valid router. check if the plugin file is complete'
                )

            # Plugin routed into target route
            target_router.include_router(plugin_router)
    except Exception as e:
        raise PluginInjectError(
            f'application level plugin {plugin} route injection failed: {str(e)}') from e


def build_final_router() -> APIRouter:
    """Build final route"""

    extra_plugins = []
    app_plugins = []

    for plugin in get_plugins():
        data = load_plugin_config(plugin)
        (extra_plugins if data.get('api') else app_plugins).append((plugin, data))

    for plugin, data in extra_plugins:
        inject_extra_router(plugin, data)

    # Main route, must be imported after injection of plugin route
    from backend.app.router import router as main_router

    for plugin, data in app_plugins:
        inject_app_router(plugin, data, main_router)

    return main_router


def _install_plugin_requirements(plugin: str, requirements_file: str) -> None:
    """
    Dependence on installing a single plugin

    :param plugin: plugin name
    :param _other organiser
    :return:
    """
    try:
        ensurepip_install = [sys.executable, '-m', 'ensurepip', '--upgrade']
        pip_install = [sys.executable, '-m', 'pip',
                       'install', '-r', requirements_file]
        if settings.PLUGIN_PIP_CHINA:
            pip_install.extend(['-i', settings.PLUGIN_PIP_INDEX_URL])
        subprocess.check_call(ensurepip_install)
        subprocess.check_call(pip_install)
    except subprocess.CalledProcessError as e:
        raise PluginInjectError(
            f'plugin {plugin} relies on installation failure: {e.stderr}') from e


def install_requirements() -> None:
    """Install plugin dependent"""
    for plugin in get_plugins():
        requirements_file = os.path.join(
            PLUGIN_DIR, plugin, 'requirements.txt')
        if os.path.exists(requirements_file):
            _install_plugin_requirements(plugin, requirements_file)


async def install_requirements_async() -> None:
    """
    Step installation plugin dependent

    Owing to the Windows platform constraints, it is not possible to achieve a perfect all-step scenario, details：
    https://stackoverflow.com/questions/44633458/why-am-i-getting-notimplementederror-with-async-and-await-on-windows
    """
    await run_in_threadpool(install_requirements)
