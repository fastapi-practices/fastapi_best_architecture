#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING, Any, Generic, Sequence, TypeVar

from fastapi import Depends, Query
from fastapi_pagination import pagination_ctx
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_pagination.links.bases import create_links
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from sqlalchemy import Select
    from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
SchemaT = TypeVar('SchemaT')


class _CustomPageParams(BaseModel, AbstractParams):
    """自定义分页参数"""

    page: int = Query(1, ge=1, description='页码')
    size: int = Query(20, gt=0, le=200, description='每页数量')

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class _Links(BaseModel):
    """分页链接"""

    first: str = Field(description='首页链接')
    last: str = Field(description='尾页链接')
    self: str = Field(description='当前页链接')
    next: str | None = Field(None, description='下一页链接')
    prev: str | None = Field(None, description='上一页链接')


class _PageDetails(BaseModel):
    """分页详情"""

    items: list = Field([], description='当前页数据列表')
    total: int = Field(description='数据总条数')
    page: int = Field(description='当前页码')
    size: int = Field(description='每页数量')
    total_pages: int = Field(description='总页数')
    links: _Links = Field(description='分页链接')


class _CustomPage(_PageDetails, AbstractPage[T], Generic[T]):
    """自定义分页类"""

    __params_type__ = _CustomPageParams

    @classmethod
    def create(
        cls,
        items: list,
        params: _CustomPageParams,
        total: int = 0,
    ) -> _CustomPage[T]:
        page = params.page
        size = params.size
        total_pages = ceil(total / size)
        links = create_links(
            first={'page': 1, 'size': size},
            last={'page': total_pages, 'size': size} if total > 0 else {'page': 1, 'size': size},
            next={'page': page + 1, 'size': size} if (page + 1) <= total_pages else None,
            prev={'page': page - 1, 'size': size} if (page - 1) >= 1 else None,
        ).model_dump()

        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            total_pages=total_pages,
            links=links,  # type: ignore
        )


class PageData(_PageDetails, Generic[SchemaT]):
    """
    包含返回数据 schema 的统一返回模型，仅适用于分页接口

    E.g. ::

        @router.get('/test', response_model=ResponseSchemaModel[PageData[GetApiDetail]])
        def test():
            return ResponseSchemaModel[PageData[GetApiDetail]](data=GetApiDetail(...))


        @router.get('/test')
        def test() -> ResponseSchemaModel[PageData[GetApiDetail]]:
            return ResponseSchemaModel[PageData[GetApiDetail]](data=GetApiDetail(...))


        @router.get('/test')
        def test() -> ResponseSchemaModel[PageData[GetApiDetail]]:
            res = CustomResponseCode.HTTP_200
            return ResponseSchemaModel[PageData[GetApiDetail]](code=res.code, msg=res.msg, data=GetApiDetail(...))
    """

    items: Sequence[SchemaT]


async def paging_data(db: AsyncSession, select: Select) -> dict:
    """
    基于 SQLAlchemy 创建分页数据

    :param db:
    :param select:
    :return:
    """
    paginated_data: _CustomPage = await paginate(db, select)
    
    # 【！重要】处理所有动态字段（不限于c1-c20, n1-n20）
    # 获取原始数据并保留所有字段，包括动态添加的属性
    page_data = paginated_data.model_dump()
    
    # 确保items中的每个对象都保留其所有属性（包括所有动态字段）
    if 'items' in page_data and page_data['items']:
        for i, item in enumerate(page_data['items']):
            # 检查原始对象是否有__dict__属性（SQLAlchemy模型对象通常有）
            if hasattr(paginated_data.items[i], '__dict__'):
                # 获取原始对象的所有属性
                obj_dict = paginated_data.items[i].__dict__
                # 添加所有属性（排除SQLAlchemy内部属性）
                for key, value in obj_dict.items():
                    # 排除SQLAlchemy内部属性（以_开头）和已存在的属性
                    if not key.startswith('_') and key not in item:
                        item[key] = value
                
                # 递归处理嵌套对象中的动态字段
                for key, value in item.items():
                    # 处理嵌套字典
                    if isinstance(value, dict):
                        _process_nested_dict(paginated_data.items[i], key, value)
                    # 处理嵌套列表
                    elif isinstance(value, list):
                        _process_nested_list(paginated_data.items[i], key, value)
    
    return page_data

def _process_nested_dict(original_obj, key, dict_value):
    """递归处理嵌套字典中的动态字段"""
    # 检查原始对象中对应的属性是否存在
    if hasattr(original_obj, key) and hasattr(getattr(original_obj, key), '__dict__'):
        original_nested = getattr(original_obj, key)
        nested_dict = original_nested.__dict__
        
        # 添加所有属性（排除SQLAlchemy内部属性）
        for nested_key, nested_value in nested_dict.items():
            if not nested_key.startswith('_') and nested_key not in dict_value:
                dict_value[nested_key] = nested_value
        
        # 继续递归处理更深层次的嵌套
        for nested_key, nested_value in dict_value.items():
            if isinstance(nested_value, dict):
                _process_nested_dict(original_nested, nested_key, nested_value)
            elif isinstance(nested_value, list):
                _process_nested_list(original_nested, nested_key, nested_value)

def _process_nested_list(original_obj, key, list_value):
    """递归处理嵌套列表中的动态字段"""
    # 检查原始对象中对应的属性是否存在
    if hasattr(original_obj, key) and isinstance(getattr(original_obj, key), list):
        original_list = getattr(original_obj, key)
        
        # 处理列表中的每个元素
        for i, item in enumerate(list_value):
            if i < len(original_list):
                original_item = original_list[i]
                
                # 处理字典类型的列表元素
                if isinstance(item, dict) and hasattr(original_item, '__dict__'):
                    item_dict = original_item.__dict__
                    
                    # 添加所有属性（排除SQLAlchemy内部属性）
                    for item_key, item_value in item_dict.items():
                        if not item_key.startswith('_') and item_key not in item:
                            item[item_key] = item_value
                    
                    # 继续递归处理更深层次的嵌套
                    for item_key, item_value in item.items():
                        if isinstance(item_value, dict):
                            _process_nested_dict(original_item, item_key, item_value)
                        elif isinstance(item_value, list):
                            _process_nested_list(original_item, item_key, item_value)


# 分页依赖注入
DependsPagination = Depends(pagination_ctx(_CustomPage))
