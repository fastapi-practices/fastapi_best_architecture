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
from backend.plugin.api_testing.api.v1.project import router as project_router
from backend.plugin.api_testing.api.v1.test_case import router as test_case_router
from backend.plugin.api_testing.api.v1.test_step import router as test_step_router
from backend.plugin.api_testing.api.v1.test_report import router as test_report_router

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/api_testing', tags=['接口自动化测试'])

# 数据管理接口
v1.include_router(project_router, prefix='/projects', tags=['项目管理'])
v1.include_router(test_case_router, prefix='/test_cases', tags=['测试用例管理'])
v1.include_router(test_step_router, prefix='/test_steps', tags=['测试步骤管理'])
v1.include_router(test_report_router, prefix='/test_reports', tags=['测试报告管理'])

# 功能接口
v1.include_router(request_router, prefix='/requests', tags=['请求发送'])
v1.include_router(assertion_router, prefix='/assertions', tags=['断言验证'])
v1.include_router(sql_router, prefix='/sql', tags=['SQL执行'])
v1.include_router(report_router, prefix='/reports', tags=['报告生成'])
v1.include_router(environment_router, prefix='/environments', tags=['环境管理'])
v1.include_router(mock_router, prefix='/mocks', tags=['Mock服务'])
v1.include_router(data_driven_router, prefix='/data_driven', tags=['数据驱动'])
v1.include_router(history_router, prefix='/history', tags=['历史记录'])