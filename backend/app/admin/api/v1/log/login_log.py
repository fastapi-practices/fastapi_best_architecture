#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.app.admin.schema.login_log import GetLoginLogListDetails
from backend.app.admin.service.login_log_service import login_log_service
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db_mysql import CurrentSession

router = APIRouter()


@router.get(
    '',
    summary='（模糊条件）分页获取登录日志',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_login_logs(
    db: CurrentSession,
    username: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
    ip: Annotated[str | None, Query()] = None,
) -> ResponseModel:
    log_select = await login_log_service.get_select(username=username, status=status, ip=ip)
    page_data = await paging_data(db, log_select, GetLoginLogListDetails)
    return await response_base.success(data=page_data)


@router.delete(
    '',
    summary='（批量）删除登录日志',
    dependencies=[
        Depends(RequestPermission('log:login:del')),
        DependsRBAC,
    ],
)
async def delete_login_log(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await login_log_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '/all',
    summary='清空登录日志',
    dependencies=[
        Depends(RequestPermission('log:login:empty')),
        DependsRBAC,
    ],
)
async def delete_all_login_logs() -> ResponseModel:
    count = await login_log_service.delete_all()
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
