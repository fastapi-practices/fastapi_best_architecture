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


async def paging_data(db: AsyncSession, select: Select) -> dict[str, Any]:
    """
    基于 SQLAlchemy 创建分页数据

    :param db: 数据库会话
    :param select: SQL 查询语句
    :return:
    """
    paginated_data: _CustomPage = await apaginate(db, select)
    page_data = paginated_data.model_dump()
    return page_data


# 分页依赖注入
DependsPagination = Depends(pagination_ctx(_CustomPage))
