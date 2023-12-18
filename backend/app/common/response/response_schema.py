#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict

from backend.app.common.response.response_code import CustomResponse, CustomResponseCode
from backend.app.core.conf import settings

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

        @router.get('/test')
        def test() -> ResponseModel:
            res = CustomResponseCode.HTTP_200
            return ResponseModel(code=res.code, msg=res.msg, data={'test': 'test'})
    """  # noqa: E501

    # TODO: json_encoders 配置失效: https://github.com/tiangolo/fastapi/discussions/10252
    model_config = ConfigDict(json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)})

    code: int = CustomResponseCode.HTTP_200.code
    msg: str = CustomResponseCode.HTTP_200.msg
    data: Any | None = None


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
        res: CustomResponseCode | CustomResponse = None,
        data: Any | None = None,
        exclude: _ExcludeData | None = None,
        **kwargs,
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
            # TODO: custom_encoder 配置失效: https://github.com/tiangolo/fastapi/discussions/10252
            custom_encoder = {datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)}
            kwargs.update({'custom_encoder': custom_encoder})
            data = jsonable_encoder(data, exclude=exclude, **kwargs)
        return {'code': res.code, 'msg': res.msg, 'data': data}

    async def success(
        self,
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200,
        data: Any | None = None,
        exclude: _ExcludeData | None = None,
        **kwargs,
    ) -> dict:
        return await self.__response(res=res, data=data, exclude=exclude, **kwargs)

    async def fail(
        self,
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_400,
        data: Any = None,
        exclude: _ExcludeData | None = None,
        **kwargs,
    ) -> dict:
        return await self.__response(res=res, data=data, exclude=exclude, **kwargs)


response_base = ResponseBase()
