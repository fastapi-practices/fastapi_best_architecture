#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.task_demo import router as task_demo_router
from backend.app.api.v1.sys_config import router as sys_config_router

v1 = APIRouter(prefix='/v1')

v1.include_router(auth_router)

v1.include_router(task_demo_router, prefix='/tasks', tags=['任务管理'])

v1.include_router(sys_config_router, prefix='/configs', tags=['系统配置'])
