from collections.abc import Sequence
from decimal import Decimal
from typing import Any, TypeVar

from fastapi.encoders import decimal_encoder
from msgspec import json
from sqlalchemy import Row, RowMapping
from sqlalchemy.orm import ColumnProperty, SynonymProperty, class_mapper
from starlette.responses import JSONResponse

RowData = Row | RowMapping | Any

R = TypeVar('R', bound=RowData)


def select_columns_serialize(row: R) -> dict[str, Any]:
    """
    序列化 SQLAlchemy 查询表的列，不包含关联列

    :param row: SQLAlchemy 查询结果行
    :return:
    """
    result = {}
    for column in row.__table__.columns.keys():
        value = getattr(row, column)
        if isinstance(value, Decimal):
            value = decimal_encoder(value)
        result[column] = value
    return result


def select_list_serialize(row: Sequence[R]) -> list[dict[str, Any]]:
    """
    序列化 SQLAlchemy 查询列表

    :param row: SQLAlchemy 查询结果列表
    :return:
    """
    return [select_columns_serialize(item) for item in row]


def select_as_dict(row: R, *, use_alias: bool = False) -> dict[str, Any]:
    """
    将 SQLAlchemy 查询结果转换为字典，可以包含关联数据

    :param row: SQLAlchemy 查询结果行
    :param use_alias: 是否使用别名作为列名
    :return:
    """
    if not use_alias:
        result = row.__dict__
        if '_sa_instance_state' in result:
            del result['_sa_instance_state']
    else:
        result = {}
        mapper = class_mapper(row.__class__)  # type: ignore
        for prop in mapper.iterate_properties:
            if isinstance(prop, (ColumnProperty, SynonymProperty)):
                key = prop.key
                result[key] = getattr(row, key)

    return result


class MsgSpecJSONResponse(JSONResponse):
    """
    使用高性能的 msgspec 库将数据序列化为 JSON 的响应类
    """

    def render(self, content: Any) -> bytes:
        return json.encode(content)
