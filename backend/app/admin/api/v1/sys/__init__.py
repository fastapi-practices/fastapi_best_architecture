#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.admin.api.v1.sys.config import router as config_router
from backend.app.admin.api.v1.sys.data_rule import router as data_rule_router
from backend.app.admin.api.v1.sys.dept import router as dept_router
from backend.app.admin.api.v1.sys.dict_data import router as dict_data_router
from backend.app.admin.api.v1.sys.dict_type import router as dict_type_router
from backend.app.admin.api.v1.sys.menu import router as menu_router
from backend.app.admin.api.v1.sys.plugin import router as plugin_router
from backend.app.admin.api.v1.sys.role import router as role_router
from backend.app.admin.api.v1.sys.token import router as token_router
from backend.app.admin.api.v1.sys.upload import router as upload_router
from backend.app.admin.api.v1.sys.user import router as user_router

router = APIRouter(prefix='/sys')

router.include_router(config_router, prefix='/configs', tags=['系统配置'])
router.include_router(dept_router, prefix='/depts', tags=['系统部门'])
router.include_router(dict_data_router, prefix='/dict-datas', tags=['系统字典数据'])
router.include_router(dict_type_router, prefix='/dict-types', tags=['系统字典类型'])
router.include_router(menu_router, prefix='/menus', tags=['系统菜单'])
router.include_router(role_router, prefix='/roles', tags=['系统角色'])
router.include_router(user_router, prefix='/users', tags=['系统用户'])
router.include_router(data_rule_router, prefix='/data-rules', tags=['系统数据权限规则'])
router.include_router(token_router, prefix='/tokens', tags=['系统令牌'])
router.include_router(upload_router, prefix='/upload', tags=['系统上传'])
router.include_router(plugin_router, prefix='/plugin', tags=['系统插件'])
