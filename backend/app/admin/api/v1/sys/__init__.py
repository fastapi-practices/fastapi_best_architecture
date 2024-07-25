#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.admin.api.v1.sys.api import router as api_router
from backend.app.admin.api.v1.sys.casbin import router as casbin_router
from backend.app.admin.api.v1.sys.config import router as config_router
from backend.app.admin.api.v1.sys.dept import router as dept_router
from backend.app.admin.api.v1.sys.dict_data import router as dict_data_router
from backend.app.admin.api.v1.sys.dict_type import router as dict_type_router
from backend.app.admin.api.v1.sys.menu import router as menu_router
from backend.app.admin.api.v1.sys.role import router as role_router
from backend.app.admin.api.v1.sys.user import router as user_router

router = APIRouter(prefix='/sys')

router.include_router(api_router, prefix='/apis', tags=['系统API'])
router.include_router(casbin_router, prefix='/casbin', tags=['系统Casbin权限'])
router.include_router(config_router, prefix='/configs', tags=['系统配置'])
router.include_router(dept_router, prefix='/depts', tags=['系统部门'])
router.include_router(dict_data_router, prefix='/dict_datas', tags=['系统字典数据'])
router.include_router(dict_type_router, prefix='/dict_types', tags=['系统字典类型'])
router.include_router(menu_router, prefix='/menus', tags=['系统目录'])
router.include_router(role_router, prefix='/roles', tags=['系统角色'])
router.include_router(user_router, prefix='/users', tags=['系统用户'])
