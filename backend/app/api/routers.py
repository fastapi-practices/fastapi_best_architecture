#!/usr/bin/env python3
# _*_ coding: utf_8 _*_
from fastapi import APIRouter

from backend.app.core.conf import settings
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.user import router as user_router
from backend.app.api.v1.casbin import router as casbin_router
from backend.app.api.v1.dept import router as dept_router
from backend.app.api.v1.role import router as role_router
from backend.app.api.v1.menu import router as menu_router
from backend.app.api.v1.api import router as api_router
from backend.app.api.v1.login_log import router as login_log_router
from backend.app.api.v1.opera_log import router as opera_log_router
from backend.app.api.v1.dict_type import router as dict_type_router
from backend.app.api.v1.dict_data import router as dict_data_router
from backend.app.api.v1.mixed import router as mixed_router

v1 = APIRouter(prefix=settings.API_V1_STR)

v1.include_router(auth_router, prefix='/auth', tags=['认证'])
v1.include_router(user_router, prefix='/user', tags=['用户管理'])
v1.include_router(casbin_router, prefix='/casbin', tags=['权限管理'])
v1.include_router(dept_router, prefix='/dept', tags=['部门管理'])
v1.include_router(role_router, prefix='/role', tags=['角色管理'])
v1.include_router(menu_router, prefix='/menu', tags=['菜单管理'])
v1.include_router(api_router, prefix='/api', tags=['API管理'])
v1.include_router(dict_type_router, prefix='/dict_type', tags=['字典类型管理'])
v1.include_router(dict_data_router, prefix='/dict_data', tags=['字典数据管理'])
v1.include_router(login_log_router, prefix='/login_log', tags=['登录日志管理'])
v1.include_router(opera_log_router, prefix='/opera_log', tags=['操作日志管理'])
v1.include_router(mixed_router, prefix='/mixes', tags=['杂项'])
