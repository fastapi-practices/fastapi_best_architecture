#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.common.jwt import DependsUser
from backend.app.common.pagination import paging_data, PageDepends
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.login_log import GetAllLoginLog
from backend.app.services.login_log_service import LoginLogService

router = APIRouter()


@router.get('', summary='获取所有登录日志', dependencies=[DependsUser, PageDepends])
async def get_all_login_logs(db: CurrentSession):
    log_select = await LoginLogService.get_select()
    page_data = await paging_data(db, log_select, GetAllLoginLog)
    return response_base.success(data=page_data)
