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
    """Customize page break parameters"""

    page: int = Query(1, ge=1, description='Page Number')
    size: int = Query(20, gt=0, le=200, description='Number per page')

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class _Links(BaseModel):
    """Page Break Link"""

    first: str = Field(description='First Page Link')
    last: str = Field(description='End Page Link')
    self: str = Field(description='Current Page Link')
    next: str | None = Field(None, description='Next Page Link')
    prev: str | None = Field(None, description='Previous Page Link')


class _PageDetails(BaseModel):
    """Page Break Details"""

    items: list = Field([], description='Current Page Data List')
    total: int = Field(description='Total number of data entries')
    page: int = Field(description='Current Page Number')
    size: int = Field(description='Number per page')
    total_pages: int = Field(description='Total pages')
    links: _Links = Field(description='Page Break Link')


class _CustomPage(_PageDetails, AbstractPage[T], Generic[T]):
    """Customise Page Break Classes"""

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
    a unified return model with returned data, only for page breaks

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
    Create page break data based on SQLAlchemy

    :param db: database session
    :param self: SQL query statement
    :return:
    """
    paginated_data: _CustomPage = await apaginate(db, select)
    page_data = paginated_data.model_dump()
    return page_data


# Page break depends on injection
DependsPagination = Depends(pagination_ctx(_CustomPage))
