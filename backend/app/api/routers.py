#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1.api import router as api_router
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.casbin import router as casbin_router
from backend.app.api.v1.dept import router as dept_router
from backend.app.api.v1.dict_data import router as dict_data_router
from backend.app.api.v1.dict_type import router as dict_type_router
from backend.app.api.v1.log import router as log_router
from backend.app.api.v1.menu import router as menu_router
from backend.app.api.v1.mixed import router as mixed_router
from backend.app.api.v1.monitor import router as monitor_router
from backend.app.api.v1.role import router as role_router
from backend.app.api.v1.task import router as task_router
from backend.app.api.v1.user import router as user_router
from backend.app.core.conf import settings

v1 = APIRouter(prefix=settings.API_V1_STR)

v1.include_router(auth_router, prefix='/auth', tags=['认证'])
v1.include_router(user_router, prefix='/users', tags=['用户管理'])
v1.include_router(casbin_router, prefix='/casbin', tags=['权限管理'])
v1.include_router(dept_router, prefix='/depts', tags=['部门管理'])
v1.include_router(role_router, prefix='/roles', tags=['角色管理'])
v1.include_router(menu_router, prefix='/menus', tags=['菜单管理'])
v1.include_router(api_router, prefix='/apis', tags=['API管理'])
v1.include_router(dict_type_router, prefix='/dict-types', tags=['字典类型管理'])
v1.include_router(dict_data_router, prefix='/dict-datas', tags=['字典数据管理'])
v1.include_router(log_router, prefix='/logs', tags=['日志管理'])
v1.include_router(monitor_router, prefix='/monitors', tags=['监控管理'])
v1.include_router(task_router, prefix='/tasks', tags=['任务管理'])
v1.include_router(mixed_router, prefix='/mixes', tags=['杂项'])
