import warnings

from typing import Any

from pydantic import BaseModel, Field, field_validator

from backend.common.enums import PluginLevelType
from backend.plugin.errors import PluginConfigError
from backend.utils.pattern_validate import match_string

# 支持的标签类型
_VALID_TAGS = frozenset({'ai', 'mcp', 'agent', 'auth', 'storage', 'notification', 'task', 'payment', 'other'})

# 支持的数据库类型
_VALID_DATABASES = frozenset({'mysql', 'postgresql'})


class PluginInfoSchema(BaseModel):
    """插件信息模型"""

    icon: str | None = Field(default=None, description='图标路径或链接地址')
    summary: str = Field(..., min_length=1, max_length=100, description='摘要')
    version: str = Field(..., description='版本号')
    description: str = Field(..., min_length=1, max_length=500, description='描述')
    author: str = Field(..., min_length=1, max_length=50, description='作者')
    tags: list[str] = Field(default_factory=list, description='标签')
    database: list[str] = Field(default_factory=list, description='数据库支持')

    @field_validator('version')
    @classmethod
    def validate_version(cls, v: str) -> str:
        """校验版本号格式"""
        if not match_string(r'^\d+\.\d+\.\d+$', v):
            raise PluginConfigError(f'版本号格式错误，应为 x.y.z 格式，如 1.0.0，当前值: {v}')
        return v

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        """校验标签"""
        if v:
            invalid_tags = set(v) - _VALID_TAGS
            if invalid_tags:
                raise PluginConfigError(
                    f'标签值无效: {", ".join(invalid_tags)}，支持的标签: {", ".join(sorted(_VALID_TAGS))}'
                )
        return v

    @field_validator('database')
    @classmethod
    def validate_database(cls, v: list[str]) -> list[str]:
        """校验数据库类型"""
        if v:
            invalid_dbs = set(v) - _VALID_DATABASES
            if invalid_dbs:
                raise PluginConfigError(
                    f'数据库类型无效: {", ".join(invalid_dbs)}，支持的数据库: {", ".join(sorted(_VALID_DATABASES))}'
                )
        return v


class AppPluginAppSchema(BaseModel):
    """应用级插件 app 配置模型"""

    router: list[str] = Field(..., min_length=1, description='路由器实例列表')

    @field_validator('router')
    @classmethod
    def validate_router(cls, v: list[str]) -> list[str]:
        """校验路由器配置"""
        if not v:
            raise PluginConfigError('router 配置不能为空')
        for router in v:
            if not router or not isinstance(router, str):
                raise PluginConfigError(f'router 配置项必须为非空字符串，当前值: {router}')
        return v


class ExtendPluginAppSchema(BaseModel):
    """扩展级插件 app 配置模型"""

    extend: str = Field(..., min_length=1, description='扩展的应用文件夹名称')


class ApiConfigSchema(BaseModel):
    """API 配置模型"""

    prefix: str = Field(..., min_length=1, description='路由前缀')
    tags: str = Field(..., min_length=1, description='Swagger 文档标签')

    @field_validator('prefix')
    @classmethod
    def validate_prefix(cls, v: str) -> str:
        """校验路由前缀"""
        if not v.startswith('/'):
            raise PluginConfigError(f'路由前缀必须以 "/" 开头，当前值: {v}')
        if not match_string(r'^/[a-zA-Z0-9_/-]*$', v):
            raise PluginConfigError(f'路由前缀格式错误，只能包含字母、数字、下划线、斜杠和连字符，当前值: {v}')
        return v


class AppPluginConfigSchema(BaseModel):
    """应用级插件配置模型"""

    plugin: PluginInfoSchema = Field(..., description='插件信息')
    app: AppPluginAppSchema = Field(..., description='应用配置')
    settings: dict[str, Any] = Field(default_factory=dict, description='配置项')

    @field_validator('settings')
    @classmethod
    def validate_settings(cls, v: dict[str, Any]) -> dict[str, Any]:
        """校验配置项名称必须全大写"""
        if v:
            invalid_keys = [key for key in v if not key.isupper()]
            if invalid_keys:
                raise PluginConfigError(f'settings 配置项名称必须全大写，无效的配置项: {", ".join(invalid_keys)}')
        return v


class ExtendPluginConfigSchema(BaseModel):
    """扩展级插件配置模型"""

    plugin: PluginInfoSchema = Field(..., description='插件信息')
    app: ExtendPluginAppSchema = Field(..., description='应用配置')
    api: dict[str, ApiConfigSchema] = Field(..., min_length=1, description='接口配置')
    settings: dict[str, Any] = Field(default_factory=dict, description='配置项')

    @field_validator('api', mode='before')
    @classmethod
    def validate_api_config(cls, v: dict[str, Any]) -> dict[str, ApiConfigSchema]:
        """校验并转换 API 配置"""
        if not v:
            raise PluginConfigError('扩展级插件必须包含至少一个 api 配置')
        validated_api = {}
        for api_name, api_config in v.items():
            if not api_name or not isinstance(api_name, str):
                raise PluginConfigError(f'api 配置名称必须为非空字符串，当前值: {api_name}')
            if not match_string(r'^[a-zA-Z_][a-zA-Z0-9_]*$', api_name):
                raise PluginConfigError(
                    f'api 配置名称格式错误，必须以字母或下划线开头，只能包含字母、数字和下划线，当前值: {api_name}'
                )
            validated_api[api_name] = ApiConfigSchema(**api_config) if isinstance(api_config, dict) else api_config
        return validated_api

    @field_validator('settings')
    @classmethod
    def validate_settings(cls, v: dict[str, Any]) -> dict[str, Any]:
        """校验配置项名称必须全大写"""
        if v:
            invalid_keys = [key for key in v if not key.isupper()]
            if invalid_keys:
                raise PluginConfigError(f'settings 配置项名称必须全大写，无效的配置项: {", ".join(invalid_keys)}')
        return v


def validate_plugin_config(plugin_name: str, config: dict[str, Any]) -> PluginLevelType:
    """
    校验插件配置

    :param plugin_name: 插件名称
    :param config: 插件配置字典
    :return:
    """
    is_extend_plugin = 'api' in config

    try:
        if is_extend_plugin:
            ExtendPluginConfigSchema.model_validate(config)
            plugin_level = PluginLevelType.extend
        else:
            AppPluginConfigSchema.model_validate(config)
            plugin_level = PluginLevelType.app
    except Exception as e:
        error_msg = str(e)
        # 格式化 Pydantic 错误信息
        if hasattr(e, 'errors'):
            errors = e.errors()
            error_details = []
            for error in errors:
                loc = '.'.join(str(loc) for loc in error['loc'])
                msg = error['msg']
                error_details.append(f'{loc}: {msg}')
            error_msg = '; '.join(error_details)
        raise PluginConfigError(f'插件 {plugin_name} 配置校验失败: {error_msg}') from e

    # TODO 下个重大版本变更为必填
    plugin_info = config.get('plugin', {})
    if not plugin_info.get('tags'):
        warnings.warn(
            f"插件 '{plugin_name}' 未配置 'tags' 字段，该字段将在下个重大版本中必填，请及时联系插件作者同步更新",
            FutureWarning,
            stacklevel=2,
        )
    if not plugin_info.get('database'):
        warnings.warn(
            f"插件 '{plugin_name}' 未配置 'database' 字段，该字段将在下个重大版本中必填，请及时联系插件作者同步更新",
            FutureWarning,
            stacklevel=2,
        )

    return plugin_level
