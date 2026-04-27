import inspect
import json
import os
import warnings

from functools import lru_cache
from typing import Any

import anyio
import rtoml

from fastapi import APIRouter, Depends, FastAPI, Request

from backend.common.dataclasses import PluginEntry
from backend.common.enums import DataBaseType, LifespanStage, PluginLevelType, PrimaryKeyType, StatusType
from backend.common.exception import errors
from backend.common.lifespan import lifespan_manager
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR
from backend.database.redis import RedisCli, redis_client
from backend.plugin.errors import PluginConfigError, PluginInjectError
from backend.plugin.validator import validate_plugin_config
from backend.utils.async_helper import run_await
from backend.utils.dynamic_import import get_model_objects, import_module_cached


def check_plugin_installed(plugin_name: str) -> bool:
    """
    检查插件是否已安装

    :param plugin_name: 插件名称
    :return:
    """
    return (PLUGIN_DIR / plugin_name / '__init__.py').exists()


def get_required_plugins() -> tuple[str, ...]:
    """获取必需插件列表"""
    required_plugins = list(settings.PLUGIN_REQUIRED)
    if not settings.RBAC_ROLE_MENU_MODE and 'casbin_rbac' not in required_plugins:
        required_plugins.append('casbin_rbac')
    return tuple(required_plugins)


def check_required_plugins() -> None:
    """检查必需插件"""
    required_plugins = get_required_plugins()
    missing_plugins = [name for name in required_plugins if not check_plugin_installed(name)]
    if missing_plugins:
        raise PluginInjectError(f'当前系统缺少以下插件: {", ".join(missing_plugins)}，请先安装对应插件')


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


def get_enabled_plugins(plugins: tuple[str, ...] | None = None) -> set[str]:
    """
    获取已启用的插件列表

    :param plugins: 插件名称列表
    :return:
    """
    plugin_names = plugins or get_plugins()
    enabled_plugins = set(plugin_names)

    current_redis_client = RedisCli()
    run_await(current_redis_client.init)()

    try:
        for plugin in plugin_names:
            plugin_info = run_await(current_redis_client.get)(f'{settings.PLUGIN_REDIS_PREFIX}:{plugin}')
            if get_plugin_enable(plugin_info, StatusType.enable.value) != str(StatusType.enable.value):
                enabled_plugins.discard(plugin)
    finally:
        run_await(current_redis_client.aclose)()

    return enabled_plugins


def get_plugin_enable(plugin_info: str | None, default_status: int) -> str:
    """
    解析插件启用状态

    :param plugin_info: 插件缓存信息
    :param default_status: 默认状态值
    :return:
    """
    if not plugin_info:
        return str(default_status)

    try:
        return json.loads(plugin_info)['plugin']['enable']
    except Exception:
        return str(default_status)


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


def parse_plugin_config() -> tuple[list[PluginEntry], list[PluginEntry]]:
    """解析插件配置"""
    plugins = get_plugins()
    extend_plugins: list[PluginEntry] = []
    app_plugins: list[PluginEntry] = []

    # 使用独立连接
    current_redis_client = RedisCli()
    run_await(current_redis_client.init)()

    try:
        # 清理未知插件信息
        exclude_keys = [f'{settings.PLUGIN_REDIS_PREFIX}:{key}' for key in plugins]
        run_await(current_redis_client.delete_prefix)(
            settings.PLUGIN_REDIS_PREFIX,
            exclude=exclude_keys,
        )

        for plugin in plugins:
            plugin_config = load_plugin_config(plugin)
            plugin_type = validate_plugin_config(plugin, plugin_config)

            # 补充插件信息
            plugin_config['plugin']['name'] = plugin
            plugin_cache_key = f'{settings.PLUGIN_REDIS_PREFIX}:{plugin}'
            plugin_cache_info = run_await(current_redis_client.get)(plugin_cache_key)
            plugin_config['plugin']['enable'] = get_plugin_enable(plugin_cache_info, StatusType.enable.value)

            plugin_entry = PluginEntry(
                name=plugin,
                depends_on=plugin_config['plugin'].get('depends_on'),
                extend=plugin_config['app']['extend'] if plugin_type == PluginLevelType.extend else None,
                routers=plugin_config['app']['router'] if plugin_type == PluginLevelType.app else None,
                api=plugin_config['api'] if plugin_type == PluginLevelType.extend else None,
            )

            if plugin_type == PluginLevelType.extend:
                extend_plugins.append(plugin_entry)
            else:
                app_plugins.append(plugin_entry)

            # 缓存最新插件信息
            run_await(current_redis_client.set)(plugin_cache_key, json.dumps(plugin_config, ensure_ascii=False))

        # 重置插件变更状态
        run_await(current_redis_client.delete)(f'{settings.PLUGIN_REDIS_PREFIX}:changed')
    finally:
        run_await(current_redis_client.aclose)()

    return extend_plugins, app_plugins


def resolve_plugin_order(plugins: list[PluginEntry]) -> list[PluginEntry]:
    """
    根据 depends_on 对插件排序

    :param plugins: 插件配置列表
    :return:
    """
    plugin_map = {plugin.name: plugin for plugin in plugins}
    ordered_plugins: list[PluginEntry] = []
    visited: set[str] = set()
    visiting: list[str] = []

    def visit(plugin: PluginEntry) -> None:
        if plugin.name in visited:
            return
        if plugin.name in visiting:
            cycle_start = visiting.index(plugin.name)
            cycle_path = [*visiting[cycle_start:], plugin.name]
            raise PluginConfigError(f'插件存在循环依赖: {" -> ".join(cycle_path)}')

        if plugin.depends_on is not None:
            visiting.append(plugin.name)
            for dep_name in plugin.depends_on:
                dep_plugin = plugin_map.get(dep_name)
                if dep_plugin is None:
                    raise PluginConfigError(f'插件 {plugin.name} 依赖插件 {dep_name}，但插件 {dep_name} 不存在')
                visit(dep_plugin)
            visiting.pop()

        visited.add(plugin.name)
        ordered_plugins.append(plugin)

    for plugin in plugins:
        visit(plugin)

    return ordered_plugins


def build_final_router() -> APIRouter:
    """构建最终路由"""
    extend_plugins, app_plugins = parse_plugin_config()
    plugins = extend_plugins + app_plugins
    ordered_plugins = resolve_plugin_order(plugins)

    for plugin in ordered_plugins:
        if plugin.api is not None:
            inject_extend_router(plugin)

    # 主路由，必须在扩展级插件路由注入后，应用级插件路由注入前导入
    from backend.app.router import router as main_router

    for plugin in ordered_plugins:
        if plugin.routers is not None:
            inject_app_router(plugin, main_router)

    return main_router


def inject_extend_router(plugin: PluginEntry) -> None:
    """
    扩展级插件路由注入

    :param plugin: 插件名称
    :return:
    """
    plugin_api_path = PLUGIN_DIR / plugin.name / 'api'
    if not os.path.exists(plugin_api_path):
        raise PluginConfigError(f'插件 {plugin.name} 缺少 api 目录，请检查插件文件是否完整')

    for root, _, api_files in os.walk(plugin_api_path):
        for file in api_files:
            if not (file.endswith('.py') and file != '__init__.py'):
                continue

            # 解析插件路由配置
            file_config = plugin.api[file[:-3]]
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
                        f'扩展级插件 {plugin.name} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整',
                        FutureWarning,
                    )
                    continue

                # 获取目标 app 路由
                relative_path = os.path.relpath(root, plugin_api_path)
                app_name = plugin.extend
                target_module_path = f'backend.app.{app_name}.api.{relative_path.replace(os.sep, ".")}'
                target_module = import_module_cached(target_module_path)
                target_router = getattr(target_module, 'router', None)

                if not target_router or not isinstance(target_router, APIRouter):
                    raise PluginInjectError(
                        f'扩展级插件 {plugin.name} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整',
                    )

                # 将插件路由注入到目标路由中
                target_router.include_router(
                    router=plugin_router,
                    prefix=prefix,
                    tags=[tags] if tags else [],
                    dependencies=[Depends(PluginStatusChecker(plugin.name))],
                )
            except Exception as e:
                raise PluginInjectError(f'扩展级插件 {plugin.name} 路由注入失败：{e!s}') from e


def inject_app_router(plugin: PluginEntry, target_router: APIRouter) -> None:
    """
    应用级插件路由注入

    :param plugin: 插件名称
    :param target_router: FastAPI 路由器
    :return:
    """
    module_path = f'backend.plugin.{plugin.name}.api.router'
    try:
        module = import_module_cached(module_path)
        routers = plugin.routers
        if not routers or not isinstance(routers, list):
            raise PluginConfigError(f'应用级插件 {plugin.name} 配置文件存在错误，请检查')

        for router in routers:
            plugin_router = getattr(module, router, None)
            if not plugin_router or not isinstance(plugin_router, APIRouter):
                raise PluginInjectError(
                    f'应用级插件 {plugin.name} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整',
                )

            # 将插件路由注入到目标路由中
            target_router.include_router(plugin_router, dependencies=[Depends(PluginStatusChecker(plugin.name))])
    except Exception as e:
        raise PluginInjectError(f'应用级插件 {plugin.name} 路由注入失败：{e!s}') from e


def register_plugin_lifespan_hook(plugin: str, module: Any) -> None:
    """
    注册插件 lifespan hook

    :param plugin: 插件名称
    :param module: 插件 hooks 模块
    :return:
    """
    lifespan_hook = getattr(module, 'lifespan', None)
    if lifespan_hook is None:
        return

    if not callable(lifespan_hook):
        log.warning(f'插件 {plugin} 的 lifespan 不是可调用对象，已跳过')
        return

    lifespan_manager.register(lifespan_hook, stage=LifespanStage.plugin)  # type: ignore[call-overload]
    log.info(f'插件 {plugin} lifespan hook 注册成功')


def run_plugin_setup_hook(plugin: str, module: Any, app: FastAPI) -> None:
    """
    执行插件 setup hook

    :param plugin: 插件名称
    :param module: 插件 hooks 模块
    :param app: FastAPI 应用实例
    :return:
    """
    setup_hook = getattr(module, 'setup', None)
    if setup_hook is None:
        return

    if not callable(setup_hook):
        log.warning(f'插件 {plugin} 的 setup 不是可调用对象，已跳过')
        return

    setup_result = setup_hook(app)
    if inspect.isawaitable(setup_result):
        run_await(lambda: setup_result)()  # type: ignore
    log.info(f'插件 {plugin} setup hook 执行成功')


def setup_plugins(app: FastAPI) -> None:
    """
    注册并执行插件 hooks

    :param app: FastAPI 应用实例
    :return:
    """
    enabled_plugins = get_enabled_plugins()
    extend_plugins, app_plugins = parse_plugin_config()
    plugins: list[PluginEntry] = [plugin for plugin in extend_plugins + app_plugins if plugin.name in enabled_plugins]

    # 按插件依赖关系排序
    try:
        ordered_plugins = resolve_plugin_order(plugins)
    except PluginConfigError as e:
        log.error(f'插件依赖解析失败: {e}')
        raise

    # 注册并执行 hooks
    for plugin in ordered_plugins:
        module_path = f'backend.plugin.{plugin.name}.hooks'
        try:
            module = import_module_cached(module_path)
        except ModuleNotFoundError as e:
            if e.name == module_path:
                continue
            log.warning(f'插件 {plugin.name} hooks 加载失败: {e}')
            continue
        except Exception as e:
            log.warning(f'插件 {plugin.name} hooks 加载失败: {e}')
            continue

        try:
            register_plugin_lifespan_hook(plugin.name, module)
            run_plugin_setup_hook(plugin.name, module, app)
        except Exception as e:
            log.exception(f'插件 {plugin.name} hooks 执行失败: {e}')
            raise PluginInjectError(f'插件 {plugin.name} hooks 执行失败：{e!s}') from e


def get_plugin_models() -> list[object]:
    """获取插件所有模型类"""
    objs = []

    for plugin in get_plugins():
        module_path = f'backend.plugin.{plugin}.model'
        model_objs = get_model_objects(module_path)
        if model_objs:
            objs.extend(model_objs)

    return objs


def build_sql_filename(
    prefix: str,
    pk_type: PrimaryKeyType,
    *,
    suffix: str | None = None,
) -> str:
    """
    构建插件 SQL 脚本文件名

    :param prefix: SQL 脚本文件名前缀，例如 init 或 destroy
    :param pk_type: 主键类型，雪花 ID 模式会追加 snowflake 标识
    :param suffix: 可选文件名后缀，追加在主键类型标识之后
    :return:
    """
    parts = [prefix]
    if pk_type == PrimaryKeyType.snowflake:
        parts.append('snowflake')
    if suffix:
        parts.append(suffix)
    return f'{"_".join(parts)}.sql'


async def get_plugin_sql(plugin: str, db_type: DataBaseType, pk_type: PrimaryKeyType) -> str | None:
    """
    获取插件 SQL 脚本

    :param plugin: 插件名称
    :param db_type: 数据库类型
    :param pk_type: 主键类型
    :return:
    """
    sql_dir = PLUGIN_DIR / plugin / 'sql' / ('mysql' if db_type == DataBaseType.mysql else 'postgresql')
    default_filename = build_sql_filename('init', pk_type)
    default_sql_file = sql_dir / default_filename
    return str(default_sql_file) if await anyio.Path(default_sql_file).exists() else None


async def get_plugin_destroy_sql(plugin: str, db_type: DataBaseType, pk_type: PrimaryKeyType) -> str | None:
    """
    获取插件销毁 SQL 脚本

    :param plugin: 插件名称
    :param db_type: 数据库类型
    :param pk_type: 主键类型
    :return:
    """
    sql_dir = PLUGIN_DIR / plugin / 'sql' / ('mysql' if db_type == DataBaseType.mysql else 'postgresql')
    sql_file = sql_dir / build_sql_filename('destroy', pk_type)
    return str(sql_file) if await anyio.Path(sql_file).exists() else None


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

        if get_plugin_enable(plugin_info, StatusType.disable.value) != str(StatusType.enable.value):
            raise errors.ServerError(msg=f'插件 {self.plugin} 未启用，请联系系统管理员')
