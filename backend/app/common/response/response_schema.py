#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from backend.app.core.conf import settings
from backend.app.utils.encoders import jsonable_encoder

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
        *, code: int = None, msg: str = None, data: Any | None = None, exclude: _ExcludeData | None = None, **kwargs
    ) -> dict:
        """
        请求成功返回通用方法

        :param code: 返回状态码
        :param msg: 返回信息
        :param data: 返回数据
        :param exclude: 返回数据字段排除
        :param kwargs: jsonable_encoder 配置项
        :return:
        """
        if data is not None:
            custom_encoder = {datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)}
            kwargs.update({'custom_encoder': custom_encoder})
            data = jsonable_encoder(data, exclude=exclude, **kwargs)
        return {'code': code, 'msg': msg, 'data': data}

    async def success(
        self, *, code=200, msg='Success', data: Any | None = None, exclude: _ExcludeData | None = None, **kwargs
    ) -> dict:
        return await self.__response(code=code, msg=msg, data=data, exclude=exclude, **kwargs)

    async def fail(
        self, *, code=400, msg='Bad Request', data: Any = None, exclude: _ExcludeData | None = None, **kwargs
    ) -> dict:
        return await self.__response(code=code, msg=msg, data=data, exclude=exclude, **kwargs)


response_base = ResponseBase()
