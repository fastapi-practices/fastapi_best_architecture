#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from backend.app.core.conf import settings
from backend.app.utils.encoders import jsonable_encoder
from backend.app.utils.serializers import select_to_dict, select_to_dict_unsafe

_ExcludeData = set[int | str] | dict[int | str, Any]

__all__ = ['ResponseModel', 'response_base']


class ResponseModel(BaseModel):
    """
    统一返回模型

    .. tip::

        如果你不想使用 ResponseBase 中的自定义编码器，可以使用此模型，返回数据将通过 fastapi 内部的编码器自动解析并返回；
        此返回模型会生成 openapi schema 文档

    E.g. ::

        @router.get('/test', response_model=ResponseModel)
        def test():
            return ResponseModel(data={'test': 'test'})

        @router.get('/test')
        def test() -> ResponseModel:
            return ResponseModel(data={'test': 'test'})
    """  # noqa: E501

    code: int = 200
    msg: str = 'Success'
    data: Any | None = None

    class Config:
        json_encoders = {datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)}


class ResponseBase:
    """
    统一返回方法

    .. tip::

        此类中的返回方法将通过自定义编码器预解析，然后由 fastapi 内部的编码器再次处理并返回，可能存在性能损耗，取决于个人喜好；
        此返回模型不会生成 openapi schema 文档

    E.g. ::

        @router.get('/test')
        def test():
            return await response_base.success(data={'test': 'test'})
    """  # noqa: E501

    @staticmethod
    async def __response(
        *,
        code: int = None,
        msg: str = None,
        data: Any | None = None,
        relationship_safe: bool = False,
        fields_safe: bool = False,
        exclude: _ExcludeData | None = None,
        **kwargs
    ) -> dict:
        """
        请求成功返回通用方法

        :param code: 返回状态码
        :param msg: 返回信息
        :param data: 返回数据
        :param exclude: 排除返回数据(data)字段
        :param relationship_safe: 关系数据安全，仅适用于 sqlalchemy 查询”关系数据“异常字段清理
        :param fields_safe: 字段安全，仅适用于 sqlalchemy 查询”字段数据“异常字段清理
        :param kwargs: jsonable_encoder 配置项
        :return:
        """
        assert (
            relationship_safe is not True or fields_safe is not True
        ), '序列化错误，relationship_safe 和 fields_safe 参数不能同时为真'
        if relationship_safe:
            data = await select_to_dict(data)
        if fields_safe:
            data = await select_to_dict_unsafe(data)
        if data is not None:
            custom_encoder = {datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)}
            kwargs.update({'custom_encoder': custom_encoder})
            data = jsonable_encoder(data, exclude=exclude, **kwargs)
        return {'code': code, 'msg': msg, 'data': data}

    async def success(
        self,
        *,
        code=200,
        msg='Success',
        data: Any | None = None,
        relationship_safe: bool = False,
        fields_safe: bool = False,
        exclude: _ExcludeData | None = None,
        **kwargs
    ) -> dict:
        result = await self.__response(
            code=code,
            msg=msg,
            data=data,
            relationship_safe=relationship_safe,
            fields_safe=fields_safe,
            exclude=exclude,
            **kwargs
        )
        return result

    async def fail(
        self,
        *,
        code=400,
        msg='Bad Request',
        data: Any = None,
        relationship_safe: bool = False,
        fields_safe: bool = False,
        exclude: _ExcludeData | None = None,
        **kwargs
    ) -> dict:
        result = await self.__response(
            code=code,
            msg=msg,
            data=data,
            relationship_safe=relationship_safe,
            fields_safe=fields_safe,
            exclude=exclude,
            **kwargs
        )
        return result


response_base = ResponseBase()
