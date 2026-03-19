from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.conf import settings
from backend.plugin.config.enums import ConfigType
from backend.plugin.config.service.config_service import config_service
from backend.plugin.core import check_plugin_installed
from backend.utils.serializers import select_list_serialize

_config_plugin_installed = check_plugin_installed('config')


if _config_plugin_installed:
    try:
        from backend.plugin.config.enums import ConfigType
        from backend.plugin.config.service.config_service import config_service
    except ImportError:
        raise ImportError('参数配置插件用法导入失败，请联系系统管理员')
else:
    ConfigType = None
    config_service = None


def _to_bool(value: str) -> bool:
    """将字符串转换为布尔值"""
    return value == 'true'


async def _load_config(
    db: AsyncSession,
    config_type: ConfigType,
    mapping: dict[str, Callable],
    status_key: str,
) -> None:
    """
    根据配置类型加载配置

    :param db: 数据库会话
    :param config_type: 配置类型枚举
    :param mapping: 配置映射 {config_key: converter}
    :param status_key: 状态键
    :return:
    """
    if not _config_plugin_installed or config_service is None:
        return

    dynamic_config = await config_service.get_all(db=db, type=config_type)
    if not dynamic_config:
        return

    config_list = select_list_serialize(dynamic_config) if hasattr(dynamic_config[0], '__table__') else dynamic_config
    configs = {dc['key']: dc['value'] for dc in config_list}
    if configs.get(status_key, '1') == '0':
        return

    for config_key, converter in mapping.items():
        if config_key in configs:
            setattr(settings, config_key, converter(configs[config_key]))


async def load_user_security_config(db: AsyncSession) -> None:
    """
    获取用户安全配置

    :param db: 数据库会话
    :return:
    """
    if ConfigType is None:
        return

    mapping = {
        'USER_LOCK_THRESHOLD': int,
        'USER_LOCK_SECONDS': int,
        'USER_PASSWORD_EXPIRY_DAYS': int,
        'USER_PASSWORD_REMINDER_DAYS': int,
        'USER_PASSWORD_HISTORY_CHECK_COUNT': int,
        'USER_PASSWORD_MIN_LENGTH': int,
        'USER_PASSWORD_MAX_LENGTH': int,
        'USER_PASSWORD_REQUIRE_SPECIAL_CHAR': _to_bool,
    }
    await _load_config(db, ConfigType.user_security, mapping, 'USER_SECURITY_CONFIG_STATUS')


async def load_login_config(db: AsyncSession) -> None:
    """
    获取登录配置

    :param db: 数据库会话
    :return:
    """
    if ConfigType is None:
        return

    mapping = {
        'LOGIN_CAPTCHA_ENABLED': _to_bool,
    }
    await _load_config(db, ConfigType.login, mapping, 'LOGIN_CONFIG_STATUS')


async def load_email_config(db: AsyncSession) -> None:
    """
    获取邮箱配置

    :param db: 数据库会话
    :return:
    """
    if ConfigType is None:
        return

    mapping = {
        'EMAIL_HOST': str,
        'EMAIL_PORT': int,
        'EMAIL_SSL': _to_bool,
        'EMAIL_USERNAME': str,
        'EMAIL_PASSWORD': str,
    }
    await _load_config(db, ConfigType.email, mapping, 'EMAIL_CONFIG_STATUS')
