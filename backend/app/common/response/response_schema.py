#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from pydantic import validate_arguments, BaseModel

from backend.app.utils.encoders import jsonable_encoder

_ExcludeData = set[int | str] | dict[int | str, Any]

__all__ = ['ResponseModel', 'response_base']


class ResponseModel(BaseModel):
    """
    统一返回模型, 可在 FastAPI 接口请求中指定 response_model 及更多操作
    """

    code: int = 200
    msg: str = 'Success'
    data: Any | None = None

    class Config:
        json_encoders = {datetime: lambda x: x.strftime('%Y-%m-%d %H:%M:%S')}


class ResponseBase:
    @staticmethod
    def __json_encoder(data: Any, exclude: _ExcludeData | None = None, **kwargs):
        custom_encoder = {datetime: lambda x: x.strftime('%Y-%m-%d %H:%M:%S')}
        kwargs.update({'custom_encoder': custom_encoder})
        return jsonable_encoder(data, exclude=exclude, **kwargs)

    @staticmethod
    @validate_arguments
    def success(
        *, code: int = 200, msg: str = 'Success', data: Any | None = None, exclude: _ExcludeData | None = None, **kwargs
    ) -> dict:
        """
        请求成功返回通用方法

        :param code: 返回状态码
        :param msg: 返回信息
        :param data: 返回数据
        :param exclude: 排除返回数据(data)字段
        :return:
        """
        data = data if data is None else ResponseBase.__json_encoder(data, exclude, **kwargs)
        return {'code': code, 'msg': msg, 'data': data}

    @staticmethod
    @validate_arguments
    def fail(
        *, code: int = 400, msg: str = 'Bad Request', data: Any = None, exclude: _ExcludeData | None = None, **kwargs
    ) -> dict:
        data = data if data is None else ResponseBase.__json_encoder(data, exclude, **kwargs)
        return {'code': code, 'msg': msg, 'data': data}


response_base = ResponseBase()
