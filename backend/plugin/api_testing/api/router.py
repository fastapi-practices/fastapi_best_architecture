#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.core.conf import settings
from backend.plugin.api_testing.api.v1.request import router as request_router
from backend.plugin.api_testing.api.v1.assertion import router as assertion_router
from backend.plugin.api_testing.api.v1.sql import router as sql_router
from backend.plugin.api_testing.api.v1.report import router as report_router
from backend.plugin.api_testing.api.v1.environment import router as environment_router
from backend.plugin.api_testing.api.v1.mock import router as mock_router
from backend.plugin.api_testing.api.v1.data_driven import router as data_driven_router
from backend.plugin.api_testing.api.v1.history import router as history_router

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/api_testing', tags=['接口自动化测试'])

v1.include_router(request_router, prefix='/requests')
v1.include_router(assertion_router, prefix='/assertions')
v1.include_router(sql_router, prefix='/sql')
v1.include_router(report_router, prefix='/reports')
v1.include_router(environment_router, prefix='/environments')
v1.include_router(mock_router, prefix='/mocks')
v1.include_router(data_driven_router, prefix='/data-driven')
v1.include_router(history_router, prefix='/history')