#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import Query, Request

from backend.app.common.pagination import paging_data
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.api import GetAllApi, CreateApi, UpdateApi
from backend.app.services.api_service import ApiService


async def get_api(pk: int):
    """获取接口详情"""
    api = await ApiService.get(pk=pk)
    return await response_base.success(data=api)


async def get_all_apis(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    method: Annotated[str | None, Query()] = None,
    path: Annotated[str | None, Query()] = None,
):
    """（模糊条件）分页获取所有接口"""
    api_select = await ApiService.get_select(name=name, method=method, path=path)
    page_data = await paging_data(db, api_select, GetAllApi)
    return await response_base.success(data=page_data)


async def create_api(request: Request, obj: CreateApi):
    """创建接口"""
    await ApiService.create(obj=obj, user_id=request.user.id)
    return await response_base.success()


async def update_api(request: Request, pk: int, obj: UpdateApi):
    """更新接口"""
    count = await ApiService.update(pk=pk, obj=obj, user_id=request.user.id)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


async def delete_api(pk: Annotated[list[int], Query(...)]):
    """（批量）删除接口"""
    count = await ApiService.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
