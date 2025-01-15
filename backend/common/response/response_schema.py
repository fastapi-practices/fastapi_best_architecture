#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from fastapi import Response
from pydantic import BaseModel, ConfigDict

from backend.common.response.response_code import CustomResponse, CustomResponseCode
from backend.core.conf import settings
from backend.utils.serializers import MsgSpecJSONResponse

_ExcludeData = set[int | str] | dict[int | str, Any]

__all__ = ['ResponseModel', 'response_base']


class ResponseModel(BaseModel):
    """
    统一返回模型

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
    def __response(*, res: CustomResponseCode | CustomResponse = None, data: Any | None = None) -> ResponseModel:
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
    ) -> ResponseModel:
        return self.__response(res=res, data=data)

    def fail(
        self,
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_400,
        data: Any = None,
    ) -> ResponseModel:
        return self.__response(res=res, data=data)

    @staticmethod
    def fast_success(
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200,
        data: Any | None = None,
    ) -> Response:
        """
        此方法是为了提高接口响应速度而创建的，如果返回数据无需进行 pydantic 解析和验证，则推荐使用，相反，请不要使用！

        .. warning::

            使用此返回方法时，不要指定接口参数 response_model，也不要在接口函数后添加箭头返回类型

        :param res:
        :param data:
        :return:
        """
        return MsgSpecJSONResponse({'code': res.code, 'msg': res.msg, 'data': data})


# 动态创建模型的辅助函数
def create_detail_response_model(data_model: Type[BaseModel]) -> Type[BaseModel]:
    # 使用 Union 允许 data 字段既可以是单个实例也可以是列表
    data_field_type = Optional[Union[data_model, List[data_model]]]

    return create_model(
        'DynamicCombinedModel',  # 新模型的名字
        __base__=ResponseModel,  # 继承自 ResponseModel
        data=(data_field_type, None)  # 更新 data 字段类型为给定的 data_model 或其列表
    )


# 定义链接信息模型
class Links(BaseModel):
    first: str= Field(..., description='首页链接')
    last: str = Field(..., description="尾页链接")
    self: str= Field(None, description="当前页链接")
    next: str= Field(None, description="下一页链接")
    prev: str|None= Field(None, description="上一页链接")


# 动态创建组合模型的辅助函数
def create_paged_response_model(item_model: Type[BaseModel]) -> Type[BaseModel]:
    # 创建内部 data 模型
    DataModel = create_model(
        'DataModel',
        items=(List[item_model], Field(default_factory=list, description="业务信息")),  # 列表，默认为空
        total=(int, Field(..., description="总条数")),
        page=(int, Field(..., description="当前页")),
        size=(int, Field(..., description="每页数量")),
        total_pages=(int, Field(..., description="总页数")),
        links=(Links, Field(..., description="跳转链接")),
    )

    # 创建最终的 end 模型
    EndModel = create_model(
        'EndModel',
        __base__=ResponseModel,  # 继承自 ResponseModel
        data=(DataModel, Field(..., description="数据详情"))  # 添加 data 字段，类型为 DataModel
    )

    return EndModel


response_base: ResponseBase = ResponseBase()
