import hashlib
import os
import subprocess
import sys

from pathlib import Path

from starlette.concurrency import run_in_threadpool

from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR
from backend.database.redis import redis_client
from backend.plugin.core import get_plugins
from backend.plugin.errors import PluginInstallError
from backend.utils.async_helper import run_await


def _is_in_virtualenv() -> bool:
    """检测当前是否在虚拟环境中运行"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)


def install_requirements(plugin: str | None) -> None:  # noqa: C901
    """
    安装插件依赖

    :param plugin: 指定插件名，否则检查所有插件
    :return:
    """
    plugins = [plugin] if plugin else get_plugins()

    for plugin in plugins:
        requirements_file = PLUGIN_DIR / plugin / 'requirements.txt'
        hash_key = f'{settings.PLUGIN_REDIS_PREFIX}:requirements_hash:{plugin}'
        cached_hash = run_await(redis_client.get)(hash_key)

        if not os.path.exists(requirements_file):
            run_await(redis_client.delete)(hash_key)
            continue

        current_hash = hashlib.sha256(Path(requirements_file).read_bytes()).hexdigest()
        if cached_hash == current_hash:
            continue

        pip_install = ['uv', 'pip', 'install', '-r', requirements_file]
        if not _is_in_virtualenv():
            pip_install.append('--system')
        if settings.PLUGIN_PIP_CHINA:
            pip_install.extend(['-i', settings.PLUGIN_PIP_INDEX_URL])

        max_retries = settings.PLUGIN_PIP_MAX_RETRY
        for attempt in range(max_retries):
            try:
                subprocess.check_call(pip_install)
                run_await(redis_client.set)(hash_key, current_hash)
                break
            except subprocess.TimeoutExpired:
                if attempt == max_retries - 1:
                    raise PluginInstallError(f'插件 {plugin} 依赖安装超时')
                continue
            except subprocess.CalledProcessError as e:
                if attempt == max_retries - 1:
                    raise PluginInstallError(f'插件 {plugin} 依赖安装失败：{e}') from e
                continue


def uninstall_requirements(plugin: str) -> None:
    """
    卸载插件依赖

    :param plugin: 插件名称
    :return:
    """
    run_await(redis_client.delete)(f'{settings.PLUGIN_REDIS_PREFIX}:requirements_hash:{plugin}')
    requirements_file = PLUGIN_DIR / plugin / 'requirements.txt'
    if os.path.exists(requirements_file):
        try:
            pip_uninstall = ['uv', 'pip', 'uninstall', '-r', str(requirements_file)]
            if not _is_in_virtualenv():
                pip_uninstall.append('--system')
            subprocess.check_call(pip_uninstall, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            raise PluginInstallError(f'插件 {plugin} 依赖卸载失败：{e}') from e


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
