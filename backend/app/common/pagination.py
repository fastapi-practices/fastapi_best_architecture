#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import math
from typing import TypeVar, Generic, Sequence, Dict, Union

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from fastapi_pagination.links.bases import create_links
from pydantic import BaseModel

T = TypeVar("T")

"""
重写分页库：fastapi-pagination 
使用方法：example link: https://github.com/uriyyo/fastapi-pagination/tree/main/examples
"""


class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(20, gt=0, le=100, description="Page size")  # 默认 20 条记录

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class Page(AbstractPage[T], Generic[T]):
    data: Sequence[T]  # 数据
    total: int  # 总数据数
    page: int  # 第n页
    size: int  # 每页数量
    total_pages: int  # 总页数
    links: Dict[str, Union[str, None]]  # 跳转链接

    __params_type__ = Params  # 使用自定义的Params

    @classmethod
    def create(
            cls,
            data: Sequence[T],
            total: int,
            params: Params,
    ) -> Page[T]:
        page = params.page
        size = params.size
        total_pages = math.ceil(total / params.size)
        links = create_links(
            **{
                "first": {"page": 1, "size": f"{size}"},
                "last": {"page": f"{math.ceil(total / params.size)}", "size": f"{size}"} if total > 0 else None,
                "next": {"page": f"{page + 1}", "size": f"{size}"} if (page + 1) <= total_pages else None,
                "prev": {"page": f"{page - 1}", "size": f"{size}"} if (page - 1) >= 1 else None
            }
        ).dict()

        return cls(
            data=data,
            total=total,
            page=params.page,
            size=params.size,
            total_pages=total_pages,
            links=links
        )
