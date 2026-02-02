import json
import os
import warnings

from functools import lru_cache
from typing import Any

import anyio
import rtoml

from fastapi import APIRouter, Depends, Request

from backend.common.enums import DataBaseType, PluginLevelType, PrimaryKeyType, StatusType
from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR
from backend.database.redis import RedisCli, redis_client
from backend.plugin.errors import PluginConfigError, PluginInjectError
from backend.plugin.validator import validate_plugin_config
from backend.utils.async_helper import run_await
from backend.utils.dynamic_import import get_model_objects, import_module_cached


@lru_cache(maxsize=128)
def get_plugins() -> tuple[str, ...]:
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

    return tuple(plugin_packages)


def get_plugin_models() -> list[object]:
    """获取插件所有模型类"""
    objs = []

    for plugin in get_plugins():
        module_path = f'backend.plugin.{plugin}.model'
        model_objs = get_model_objects(module_path)
        if model_objs:
            objs.extend(model_objs)

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
        sql_file = (
            mysql_dir / 'init.sql' if pk_type == PrimaryKeyType.autoincrement else mysql_dir / 'init_snowflake.sql'
        )
    else:
        postgresql_dir = PLUGIN_DIR / plugin / 'sql' / 'postgresql'
        sql_file = (
            postgresql_dir / 'init.sql'
            if pk_type == PrimaryKeyType.autoincrement
            else postgresql_dir / 'init_snowflake.sql'
        )

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

    # 使用独立连接
    current_redis_client = RedisCli()
    run_await(current_redis_client.init)()

    # 清理未知插件信息
    run_await(current_redis_client.delete_prefix)(
        settings.PLUGIN_REDIS_PREFIX,
        exclude=[f'{settings.PLUGIN_REDIS_PREFIX}:{key}' for key in plugins],
    )

    for plugin in plugins:
        data = load_plugin_config(plugin)
        plugin_type = validate_plugin_config(plugin, data)

        if plugin_type == PluginLevelType.extend:
            extend_plugins.append(data)
        else:
            app_plugins.append(data)

        # 补充插件信息
        data['plugin']['name'] = plugin
        plugin_cache_info = run_await(current_redis_client.get)(f'{settings.PLUGIN_REDIS_PREFIX}:{plugin}')
        if plugin_cache_info:
            data['plugin']['enable'] = json.loads(plugin_cache_info)['plugin']['enable']
        else:
            data['plugin']['enable'] = str(StatusType.enable.value)

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
                app_name = plugin.get('app', {}).get('extend')
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
