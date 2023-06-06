#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from asgiref.sync import sync_to_async
from pydantic import validate_arguments, BaseModel

from backend.app.utils.encoders import jsonable_encoder

_ExcludeData = set[int | str] | dict[int | str, Any]

__all__ = ['ResponseModel', 'response_base']


class ResponseModel(BaseModel):
    """
    统一返回模型

    .. tip::

        如果你不想使用 ResponseBase 中的自定义编码器，可以使用此模型，返回数据将通过 fastapi 内部的编码器直接自动解析并返回

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
        json_encoders = {datetime: lambda x: x.strftime('%Y-%m-%d %H:%M:%S')}


class ResponseBase:
    """
    统一返回方法

    .. tip::

        此类中的返回方法将通过自定义编码器预解析，然后由 fastapi 内部的编码器再次处理并返回，可能存在性能损耗，取决于个人喜好

    E.g. ::

        @router.get('/test')
        def test():
            return await response_base.success(data={'test': 'test'})
    """  # noqa: E501

    @staticmethod
    @sync_to_async
    def __json_encoder(data: Any, exclude: _ExcludeData | None = None, **kwargs):
        custom_encoder = {datetime: lambda x: x.strftime('%Y-%m-%d %H:%M:%S')}
        kwargs.update({'custom_encoder': custom_encoder})
        result = jsonable_encoder(data, exclude=exclude, **kwargs)
        return result

    @validate_arguments
    async def success(
        self,
        *,
        code: int = 200,
        msg: str = 'Success',
        data: Any | None = None,
        exclude: _ExcludeData | None = None,
        **kwargs
    ) -> dict:
        """
        请求成功返回通用方法

        :param code: 返回状态码
        :param msg: 返回信息
        :param data: 返回数据
        :param exclude: 排除返回数据(data)字段
        :return:
        """
        data = data if data is None else await self.__json_encoder(data, exclude, **kwargs)
        return {'code': code, 'msg': msg, 'data': data}

    @validate_arguments
    async def fail(
        self,
        *,
        code: int = 400,
        msg: str = 'Bad Request',
        data: Any = None,
        exclude: _ExcludeData | None = None,
        **kwargs
    ) -> dict:
        data = data if data is None else await self.__json_encoder(data, exclude, **kwargs)
        return {'code': code, 'msg': msg, 'data': data}


response_base = ResponseBase()
