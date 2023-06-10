#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import Query

from backend.app.common.pagination import paging_data
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.login_log import GetAllLoginLog
from backend.app.services.login_log_service import LoginLogService


async def get_all_login_logs(
    db: CurrentSession,
    username: Annotated[str | None, Query()] = None,
    status: Annotated[bool | None, Query()] = None,
    ip: Annotated[str | None, Query()] = None,
):
    """（模糊条件）分页获取登录日志"""
    log_select = await LoginLogService.get_select(username=username, status=status, ip=ip)
    page_data = await paging_data(db, log_select, GetAllLoginLog)
    return await response_base.success(data=page_data)


async def delete_login_log(pk: Annotated[list[int], Query(...)]):
    """（批量）删除登录日志"""
    count = await LoginLogService.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


async def delete_all_login_logs():
    """清空登录日志"""
    count = await LoginLogService.delete_all()
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
