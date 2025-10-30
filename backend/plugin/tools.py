import json
import os
import subprocess
import sys
import warnings

from functools import lru_cache
from importlib.metadata import PackageNotFoundError, distribution
from typing import Any

import anyio
import rtoml

from fastapi import APIRouter, Depends, Request
from packaging.requirements import Requirement
from starlette.concurrency import run_in_threadpool

from backend.common.enums import DataBaseType, PrimaryKeyType, StatusType
from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR
from backend.database.redis import RedisCli, redis_client
from backend.utils._await import run_await
from backend.utils.import_parse import get_model_objects, import_module_cached


class PluginConfigError(Exception):
    """插件信息错误"""


class PluginInjectError(Exception):
    """插件注入错误"""


class PluginInstallError(Exception):
    """插件安装错误"""


@lru_cache
def get_plugins() -> list[str]:
    """获取插件列表"""
    plugin_packages = []

    # 遍历插件目录
    for item in os.listdir(PLUGIN_DIR):
        item_path = PLUGIN_DIR / item
        if not os.path.isdir(item_path) and item == '__pycache__':
            continue

        # 检查是否为目录且包含 __init__.py 文件
        if os.path.isdir(item_path) and '__init__.py' in os.listdir(item_path):
            plugin_packages.append(item)

    return plugin_packages


def get_plugin_models() -> list[type]:
    """获取插件所有模型类"""
    objs = []

    for plugin in get_plugins():
        module_path = f'backend.plugin.{plugin}.model'
        obj = get_model_objects(module_path)
        if obj:
            objs.extend(obj)

    return objs


async def get_plugin_sql(plugin: str, db_type: DataBaseType, pk_type: PrimaryKeyType) -> str | None:
    """
    获取插件 SQL 脚本

    :param plugin: 插件名称
    :param db_type: 数据库类型
    :param pk_type: 主键类型
    :return:
    """
    if db_type == DataBaseType.mysql:
        mysql_dir = PLUGIN_DIR / plugin / 'sql' / 'mysql'
        if pk_type == PrimaryKeyType.autoincrement:
            sql_file = mysql_dir / 'init.sql'
        else:
            sql_file = mysql_dir / 'init_snowflake.sql'
    else:
        postgresql_dir = PLUGIN_DIR / plugin / 'sql' / 'postgresql'
        if pk_type == PrimaryKeyType.autoincrement:
            sql_file = postgresql_dir / 'init.sql'
        else:
            sql_file = postgresql_dir / 'init_snowflake.sql'

    path = anyio.Path(sql_file)
    if not await path.exists():
        return None

    return sql_file


def load_plugin_config(plugin: str) -> dict[str, Any]:
    """
    加载插件配置

    :param plugin: 插件名称
    :return:
    """
    toml_path = PLUGIN_DIR / plugin / 'plugin.toml'
    if not os.path.exists(toml_path):
        raise PluginInjectError(f'插件 {plugin} 缺少 plugin.toml 配置文件，请检查插件是否合法')

    with open(toml_path, encoding='utf-8') as f:
        return rtoml.load(f)


def parse_plugin_config() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """解析插件配置"""

    extend_plugins = []
    app_plugins = []

    plugins = get_plugins()

    # 使用独立单例，避免与主线程冲突
    current_redis_client = RedisCli()

    # 清理未知插件信息
    run_await(current_redis_client.delete_prefix)(
        settings.PLUGIN_REDIS_PREFIX,
        exclude=[f'{settings.PLUGIN_REDIS_PREFIX}:{key}' for key in plugins],
    )

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
            # TODO: 删除过时的 include 配置
            include = data.get('app', {}).get('include')
            if include:
                warnings.warn(
                    f'插件 {plugin} 配置 app.include 即将在未来版本中弃用，请尽快更新配置为 app.extend, 详情：https://fastapi-practices.github.io/fastapi_best_architecture_docs/plugin/dev.html#%E6%8F%92%E4%BB%B6%E9%85%8D%E7%BD%AE',
                    FutureWarning,
                )
            if not include and not data.get('app', {}).get('extend'):
                raise PluginConfigError(f'扩展级插件 {plugin} 配置文件缺少 app.extend 配置')
            extend_plugins.append(data)
        else:
            if not data.get('app', {}).get('router'):
                raise PluginConfigError(f'应用级插件 {plugin} 配置文件缺少 app.router 配置')
            app_plugins.append(data)

        # 补充插件信息
        plugin_cache_info = run_await(current_redis_client.get)(f'{settings.PLUGIN_REDIS_PREFIX}:{plugin}')
        if plugin_cache_info:
            data['plugin']['enable'] = json.loads(plugin_cache_info)['plugin']['enable']
        else:
            data['plugin']['enable'] = str(StatusType.enable.value)
        data['plugin']['name'] = plugin

        # 缓存最新插件信息
        run_await(current_redis_client.set)(
            f'{settings.PLUGIN_REDIS_PREFIX}:{plugin}',
            json.dumps(data, ensure_ascii=False),
        )

    # 重置插件变更状态
    run_await(current_redis_client.delete)(f'{settings.PLUGIN_REDIS_PREFIX}:changed')

    # 关闭连接
    run_await(current_redis_client.aclose)()

    return extend_plugins, app_plugins


def inject_extend_router(plugin: dict[str, Any]) -> None:
    """
    扩展级插件路由注入

    :param plugin: 插件名称
    :return:
    """
    plugin_name: str = plugin['plugin']['name']
    plugin_api_path = PLUGIN_DIR / plugin_name / 'api'
    if not os.path.exists(plugin_api_path):
        raise PluginConfigError(f'插件 {plugin} 缺少 api 目录，请检查插件文件是否完整')

    for root, _, api_files in os.walk(plugin_api_path):
        for file in api_files:
            if not (file.endswith('.py') and file != '__init__.py'):
                continue

            # 解析插件路由配置
            file_config = plugin['api'][file[:-3]]
            prefix = file_config['prefix']
            tags = file_config['tags']

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
                # TODO: 删除过时的 include 配置
                app_name = plugin.get('app', {}).get('include') or plugin.get('app', {}).get('extend')
                target_module_path = f'backend.app.{app_name}.api.{relative_path.replace(os.sep, ".")}'
                target_module = import_module_cached(target_module_path)
                target_router = getattr(target_module, 'router', None)

                if not target_router or not isinstance(target_router, APIRouter):
                    raise PluginInjectError(
                        f'扩展级插件 {plugin_name} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整',
                    )

                # 将插件路由注入到目标路由中
                target_router.include_router(
                    router=plugin_router,
                    prefix=prefix,
                    tags=[tags] if tags else [],
                    dependencies=[Depends(PluginStatusChecker(plugin_name))],
                )
            except Exception as e:
                raise PluginInjectError(f'扩展级插件 {plugin_name} 路由注入失败：{e!s}') from e


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
        routers = plugin['app']['router']
        if not routers or not isinstance(routers, list):
            raise PluginConfigError(f'应用级插件 {plugin_name} 配置文件存在错误，请检查')

        for router in routers:
            plugin_router = getattr(module, router, None)
            if not plugin_router or not isinstance(plugin_router, APIRouter):
                raise PluginInjectError(
                    f'应用级插件 {plugin_name} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整',
                )

            # 将插件路由注入到目标路由中
            target_router.include_router(plugin_router, dependencies=[Depends(PluginStatusChecker(plugin_name))])
    except Exception as e:
        raise PluginInjectError(f'应用级插件 {plugin_name} 路由注入失败：{e!s}') from e


def build_final_router() -> APIRouter:
    """构建最终路由"""
    extend_plugins, app_plugins = parse_plugin_config()

    for plugin in extend_plugins:
        inject_extend_router(plugin)

    # 主路由，必须在扩展级插件路由注入后，应用级插件路由注入前导入
    from backend.app.router import router as main_router

    for plugin in app_plugins:
        inject_app_router(plugin, main_router)

    return main_router


def _ensure_pip_available() -> bool:
    """确保 pip 在虚拟环境中可用"""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass

    # 尝试使用 ensurepip
    try:
        subprocess.check_call(
            [sys.executable, '-m', 'ensurepip', '--default-pip'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass

    # 尝试下载并安装
    try:
        import os
        import tempfile

        import httpx

        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                with httpx.Client(timeout=3) as client:
                    get_pip_url = 'https://bootstrap.pypa.io/get-pip.py'
                    response = client.get(get_pip_url)
                    response.raise_for_status()
                    f.write(response.text)
                    temp_file = f.name
        except Exception:  # noqa: ignore
            return False

        try:
            subprocess.check_call([sys.executable, temp_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            result = subprocess.run([sys.executable, '-m', 'pip', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        finally:
            try:
                os.unlink(temp_file)
            except OSError:
                pass
    except Exception:  # noqa: ignore
        pass

    return False


def install_requirements(plugin: str | None) -> None:  # noqa: C901
    """
    安装插件依赖

    :param plugin: 指定插件名，否则检查所有插件
    :return:
    """
    plugins = [plugin] if plugin else get_plugins()

    for plugin in plugins:
        requirements_file = PLUGIN_DIR / plugin / 'requirements.txt'
        missing_dependencies = False
        if os.path.exists(requirements_file):
            with open(requirements_file, encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    try:
                        req = Requirement(line)
                        dependency = req.name.lower()
                    except Exception as e:
                        raise PluginInstallError(f'插件 {plugin} 依赖 {line} 格式错误: {e!s}') from e
                    try:
                        distribution(dependency)
                    except PackageNotFoundError:
                        missing_dependencies = True

        if missing_dependencies:
            try:
                if not _ensure_pip_available():
                    raise PluginInstallError(f'pip 安装失败，无法继续安装插件 {plugin} 依赖')

                pip_install = [sys.executable, '-m', 'pip', 'install', '-r', requirements_file]
                if settings.PLUGIN_PIP_CHINA:
                    pip_install.extend(['-i', settings.PLUGIN_PIP_INDEX_URL])

                max_retries = settings.PLUGIN_PIP_MAX_RETRY
                for attempt in range(max_retries):
                    try:
                        subprocess.check_call(
                            pip_install,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        break
                    except subprocess.TimeoutExpired:
                        if attempt == max_retries - 1:
                            raise PluginInstallError(f'插件 {plugin} 依赖安装超时')
                        continue
                    except subprocess.CalledProcessError as e:
                        if attempt == max_retries - 1:
                            raise PluginInstallError(f'插件 {plugin} 依赖安装失败：{e}') from e
                        continue
            except subprocess.CalledProcessError as e:
                raise PluginInstallError(f'插件 {plugin} 依赖安装失败：{e}') from e


def uninstall_requirements(plugin: str) -> None:
    """
    卸载插件依赖

    :param plugin: 插件名称
    :return:
    """
    requirements_file = PLUGIN_DIR / plugin / 'requirements.txt'
    if os.path.exists(requirements_file):
        try:
            pip_uninstall = [sys.executable, '-m', 'pip', 'uninstall', '-r', requirements_file, '-y']
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
        plugin_info = await redis_client.get(f'{settings.PLUGIN_REDIS_PREFIX}:{self.plugin}')
        if not plugin_info:
            log.error('插件状态未初始化或丢失，需重启服务自动修复')
            raise PluginInjectError('插件状态未初始化或丢失，请联系系统管理员')

        if not int(json.loads(plugin_info)['plugin']['enable']):
            raise errors.ServerError(msg=f'插件 {self.plugin} 未启用，请联系系统管理员')
