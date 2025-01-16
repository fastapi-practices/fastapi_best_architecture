#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any, Generic, TypeVar

from fastapi import Response
from pydantic import BaseModel, ConfigDict

from backend.common.response.response_code import CustomResponse, CustomResponseCode
from backend.core.conf import settings
from backend.utils.serializers import MsgSpecJSONResponse

SchemaT = TypeVar('SchemaT')


class ResponseModel(BaseModel):
    """
    通用型统一返回模型，不包含 data 数据结构

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
    """

    # TODO: json_encoders 配置失效: https://github.com/tiangolo/fastapi/discussions/10252
    model_config = ConfigDict(json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)})

    code: int = CustomResponseCode.HTTP_200.code
    msg: str = CustomResponseCode.HTTP_200.msg
    data: Any | None = None


class ResponseSchemaModel(ResponseModel, Generic[SchemaT]):
    """
    包含 data schema 的统一返回模型，适用于非分页接口

    E.g. ::

        @router.get('/test', response_model=ResponseSchemaModel[GetApiListDetails])
        def test():
            return ResponseSchemaModel[GetApiListDetails](data=GetApiListDetails(...))


        @router.get('/test')
        def test() -> ResponseSchemaModel[GetApiListDetails]:
            return ResponseSchemaModel[GetApiListDetails](data=GetApiListDetails(...))


        @router.get('/test')
        def test() -> ResponseSchemaModel[GetApiListDetails]:
            res = CustomResponseCode.HTTP_200
            return ResponseSchemaModel[GetApiListDetails](code=res.code, msg=res.msg, data=GetApiListDetails(...))
    """

    data: SchemaT


class ResponseBase:
    """
    统一返回方法

    .. tip::

        此类中的方法将返回 ResponseModel 模型，作为一种编码风格而存在；

    E.g. ::

        @router.get('/test')
        def test() -> ResponseModel:
            return response_base.success(data={'test': 'test'})
    """

    @staticmethod
    def __response(
        *, res: CustomResponseCode | CustomResponse = None, data: Any | None = None
    ) -> ResponseModel | ResponseSchemaModel:
        """
        请求成功返回通用方法

        :param res: 返回信息
        :param data: 返回数据
        :return:
        """
        return ResponseModel(code=res.code, msg=res.msg, data=data)

    def success(
        self,
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200,
        data: Any | None = None,
    ) -> ResponseModel | ResponseSchemaModel:
        return self.__response(res=res, data=data)

    def fail(
        self,
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_400,
        data: Any = None,
    ) -> ResponseModel | ResponseSchemaModel:
        return self.__response(res=res, data=data)

    @staticmethod
    def fast_success(
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200,
        data: Any | None = None,
    ) -> Response | ResponseSchemaModel:
        """
        此方法是为了提高接口响应速度而创建的，如果返回数据无需进行 pydantic 解析和验证，则推荐使用，相反，请不要使用！

        .. warning::

            使用此返回方法时，不要指定接口参数 response_model，也不要在接口函数后添加箭头返回类型

        :param res:
        :param data:
        :return:
        """
        return MsgSpecJSONResponse({'code': res.code, 'msg': res.msg, 'data': data})


response_base: ResponseBase = ResponseBase()
