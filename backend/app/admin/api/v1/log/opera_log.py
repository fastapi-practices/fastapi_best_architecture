#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.app.admin.schema.opera_log import GetOperaLogDetail
from backend.app.admin.service.opera_log_service import opera_log_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.get(
    '',
    summary='Page Break for Operations Log',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_opera_logs(
    db: CurrentSession,
    username: Annotated[str | None, Query(description='Username')] = None,
    status: Annotated[int | None, Query(description='Status')] = None,
    ip: Annotated[str | None, Query(description='IP ADDRESS')] = None,
) -> ResponseSchemaModel[PageData[GetOperaLogDetail]]:
    log_select = await opera_log_service.get_select(username=username, status=status, ip=ip)
    page_data = await paging_data(db, log_select)
    return response_base.success(data=page_data)


@router.delete(
    '',
    summary='Batch Delete Operations Log',
    dependencies=[
        Depends(RequestPermission('log:opera:del')),
        DependsRBAC,
    ],
)
async def delete_opera_log(pk: Annotated[list[int], Query(description='OPERATION LOG ID LIST')]) -> ResponseModel:
    count = await opera_log_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/all',
    summary='Empty Operations Log',
    dependencies=[
        Depends(RequestPermission('log:opera:empty')),
        DependsRBAC,
    ],
)
async def delete_all_opera_logs() -> ResponseModel:
    count = await opera_log_service.delete_all()
    if count > 0:
        return response_base.success()
    return response_base.fail()
