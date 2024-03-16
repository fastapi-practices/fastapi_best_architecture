#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.admin.api.v1.sys.api import router as api_router
from backend.app.admin.api.v1.sys.casbin import router as casbin_router
from backend.app.admin.api.v1.sys.dept import router as dept_router
from backend.app.admin.api.v1.sys.dict_data import router as dict_data_router
from backend.app.admin.api.v1.sys.dict_type import router as dict_type_router
from backend.app.admin.api.v1.sys.menu import router as menu_router
from backend.app.admin.api.v1.sys.role import router as role_router
from backend.app.admin.api.v1.sys.user import router as user_router

router = APIRouter(prefix='/sys')

router.include_router(api_router, prefix='/apis', tags=['API管理'])
router.include_router(casbin_router, prefix='/casbin', tags=['Casbin权限管理'])
router.include_router(dept_router, prefix='/depts', tags=['部门管理'])
router.include_router(dict_data_router, prefix='/dict_datas', tags=['字典数据管理'])
router.include_router(dict_type_router, prefix='/dict_types', tags=['字典类型管理'])
router.include_router(menu_router, prefix='/menus', tags=['目录管理'])
router.include_router(role_router, prefix='/roles', tags=['角色管理'])
router.include_router(user_router, prefix='/users', tags=['用户管理'])
