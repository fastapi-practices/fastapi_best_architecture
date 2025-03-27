#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Generic, TypeVar

from fastapi import Response
from pydantic import BaseModel, Field

from backend.common.response.response_code import CustomResponse, CustomResponseCode
from backend.utils.serializers import MsgSpecJSONResponse

SchemaT = TypeVar('SchemaT')


class ResponseModel(BaseModel):
    """
    不包含返回数据 schema 的通用型统一返回模型

    示例::

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

    code: int = Field(CustomResponseCode.HTTP_200.code, description='返回状态码')
    msg: str = Field(CustomResponseCode.HTTP_200.msg, description='返回信息')
    data: Any | None = Field(None, description='返回数据')


class ResponseSchemaModel(ResponseModel, Generic[SchemaT]):
    """
    包含返回数据 schema 的通用型统一返回模型，仅适用于非分页接口

    示例::

        @router.get('/test', response_model=ResponseSchemaModel[GetApiDetail])
        def test():
            return ResponseSchemaModel[GetApiDetail](data=GetApiDetail(...))


        @router.get('/test')
        def test() -> ResponseSchemaModel[GetApiDetail]:
            return ResponseSchemaModel[GetApiDetail](data=GetApiDetail(...))


        @router.get('/test')
        def test() -> ResponseSchemaModel[GetApiDetail]:
            res = CustomResponseCode.HTTP_200
            return ResponseSchemaModel[GetApiDetail](code=res.code, msg=res.msg, data=GetApiDetail(...))
    """

    data: SchemaT


class ResponseBase:
    """统一返回方法"""

    @staticmethod
    def __response(
        *, res: CustomResponseCode | CustomResponse = None, data: Any | None = None
    ) -> ResponseModel | ResponseSchemaModel:
        """
        请求返回通用方法

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
        """
        成功响应

        :param res: 返回信息
        :param data: 返回数据
        :return:
        """
        return self.__response(res=res, data=data)

    def fail(
        self,
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_400,
        data: Any = None,
    ) -> ResponseModel | ResponseSchemaModel:
        """
        失败响应

        :param res: 返回信息
        :param data: 返回数据
        :return:
        """
        return self.__response(res=res, data=data)

    @staticmethod
    def fast_success(
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200,
        data: Any | None = None,
    ) -> Response:
        """
        此方法是为了提高接口响应速度而创建的，在解析较大 json 时有显著性能提升，但将丢失 pydantic 解析和验证

        .. warning::

            使用此返回方法时，不能指定接口参数 response_model 和箭头返回类型

        :param res: 返回信息
        :param data: 返回数据
        :return:
        """
        return MsgSpecJSONResponse({'code': res.code, 'msg': res.msg, 'data': data})


response_base: ResponseBase = ResponseBase()
