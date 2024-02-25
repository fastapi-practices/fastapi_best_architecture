#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.log import router as log_router
from backend.app.api.v1.mixed import router as mixed_router
from backend.app.api.v1.monitor import router as monitor_router
from backend.app.api.v1.sys import router as sys_router
from backend.app.api.v1.task import router as task_router
from backend.app.core.conf import settings

v1 = APIRouter(prefix=settings.API_V1_STR)

# 集合
v1.include_router(auth_router)
v1.include_router(sys_router)
v1.include_router(log_router)
v1.include_router(monitor_router)
v1.include_router(mixed_router)
# 独立
v1.include_router(task_router, prefix='/tasks', tags=['任务管理'])
