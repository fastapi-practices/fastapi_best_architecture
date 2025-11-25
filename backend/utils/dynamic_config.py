from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.conf import settings
from backend.database.db import async_engine
from backend.utils.serializers import select_list_serialize

_sys_config_table_exists: bool | None = None


async def check_sys_config_table_exists() -> bool:
    """
    检查 sys_config 表是否存在

    :return:
    """
    global _sys_config_table_exists
    if _sys_config_table_exists is None:
        async with async_engine.begin() as conn:
            _sys_config_table_exists = await conn.run_sync(lambda c: inspect(c).has_table('sys_config', schema=None))
    return _sys_config_table_exists


async def load_user_security_config(db: AsyncSession) -> None:  # noqa: C901
    """
    获取用户安全配置

    :param db: 数据库会话
    :return:
    """
    if not await check_sys_config_table_exists():
        return

    from backend.plugin.config.crud.crud_config import config_dao
    from backend.plugin.config.enums import ConfigType

    dynamic_config = await config_dao.get_all(db, ConfigType.user_security)

    if dynamic_config:
        security_config_status_key = 'USER_SECURITY_CONFIG_STATUS'
        lock_threshold_key = 'USER_LOCK_THRESHOLD'
        lock_seconds_key = 'USER_LOCK_SECONDS'
        password_expiry_days_key = 'USER_PASSWORD_EXPIRY_DAYS'
        password_reminder_days_key = 'USER_PASSWORD_REMINDER_DAYS'
        password_history_check_count_key = 'USER_PASSWORD_HISTORY_CHECK_COUNT'
        password_min_length_key = 'USER_PASSWORD_MIN_LENGTH'
        password_max_length_key = 'USER_PASSWORD_MAX_LENGTH'
        password_require_special_char_key = 'USER_PASSWORD_REQUIRE_SPECIAL_CHAR'

        configs = {dc['key']: dc['value'] for dc in select_list_serialize(dynamic_config)}
        if int(configs.get(security_config_status_key)):
            if lock_threshold_key in configs:
                settings.USER_LOCK_THRESHOLD = int(configs[lock_threshold_key])
            if lock_seconds_key in configs:
                settings.USER_LOCK_SECONDS = int(configs[lock_seconds_key])
            if password_expiry_days_key in configs:
                settings.USER_PASSWORD_EXPIRY_DAYS = int(configs[password_expiry_days_key])
            if password_reminder_days_key in configs:
                settings.USER_PASSWORD_REMINDER_DAYS = int(configs[password_reminder_days_key])
            if password_history_check_count_key in configs:
                settings.USER_PASSWORD_HISTORY_CHECK_COUNT = int(configs[password_history_check_count_key])
            if password_min_length_key in configs:
                settings.USER_PASSWORD_MIN_LENGTH = int(configs[password_min_length_key])
            if password_max_length_key in configs:
                settings.USER_PASSWORD_MAX_LENGTH = int(configs[password_max_length_key])
            if password_require_special_char_key in configs:
                settings.USER_PASSWORD_REQUIRE_SPECIAL_CHAR = configs[password_require_special_char_key] == 'true'


async def load_login_config(db: AsyncSession) -> None:
    """
    获取登录配置

    :param db: 数据库会话
    :return:
    """
    if not await check_sys_config_table_exists():
        return

    from backend.plugin.config.crud.crud_config import config_dao
    from backend.plugin.config.enums import ConfigType

    dynamic_config = await config_dao.get_all(db, ConfigType.login)

    if dynamic_config:
        login_config_status_key = 'LOGIN_CONFIG_STATUS'
        login_captcha_enabled_key = 'LOGIN_CAPTCHA_ENABLED'

        configs = {dc['key']: dc['value'] for dc in select_list_serialize(dynamic_config)}
        if int(configs.get(login_config_status_key)) and login_captcha_enabled_key in configs:
            settings.LOGIN_CAPTCHA_ENABLED = configs[login_captcha_enabled_key] == 'true'


async def load_email_config(db: AsyncSession) -> None:
    """
    获取邮箱配置

    :param db: 数据库会话
    :return:
    """
    if not await check_sys_config_table_exists():
        return

    from backend.plugin.config.crud.crud_config import config_dao
    from backend.plugin.config.enums import ConfigType

    dynamic_config = await config_dao.get_all(db, ConfigType.email)

    if dynamic_config:
        email_config_status_key = 'EMAIL_CONFIG_STATUS'
        host_key = 'EMAIL_HOST'
        port_key = 'EMAIL_PORT'
        ssl_key = 'EMAIL_SSL'
        username_key = 'EMAIL_USERNAME'
        password_key = 'EMAIL_PASSWORD'

        configs = {dc['key']: dc['value'] for dc in select_list_serialize(dynamic_config)}
        if int(configs.get(email_config_status_key)):
            settings.EMAIL_HOST = str(configs[host_key])
        if configs.get(port_key):
            settings.EMAIL_PORT = int(configs[port_key])
        if configs.get(ssl_key):
            settings.EMAIL_SSL = configs[ssl_key] == 'true'
        if configs.get(username_key):
            settings.EMAIL_USERNAME = str(configs[username_key])
        if configs.get(password_key):
            settings.EMAIL_PASSWORD = str(configs[password_key])
