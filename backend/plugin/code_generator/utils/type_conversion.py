from functools import lru_cache

from backend.common.enums import DataBaseType
from backend.core.conf import settings
from backend.plugin.code_generator.enums import GenMySQLColumnType, GenPostgreSQLColumnType


@lru_cache(maxsize=128)
def sql_type_to_sqlalchemy(typing: str) -> str:
    """
    将 SQL 类型转换为 SQLAlchemy 类型

    :param typing: SQL 类型字符串
    :return:
    """
    if DataBaseType.mysql == settings.DATABASE_TYPE:
        if typing in GenMySQLColumnType.get_member_keys():
            return typing
    else:
        if typing in GenPostgreSQLColumnType.get_member_keys():
            return typing
    return 'String'


@lru_cache(maxsize=128)
def sql_type_to_pydantic(typing: str) -> str:
    """
    将 SQL 类型转换为 Pydantic 类型

    :param typing: SQL 类型字符串
    :return:
    """
    try:
        if DataBaseType.mysql == settings.DATABASE_TYPE:
            return GenMySQLColumnType[typing].value
        if typing == 'CHARACTER VARYING':  # postgresql 中 DDL VARCHAR 的别名
            return 'str'
        return GenPostgreSQLColumnType[typing].value
    except KeyError:
        return 'str'
