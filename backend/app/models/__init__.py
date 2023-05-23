#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# 导入所有模型，并将 Base 放在最前面， 以便 Base 拥有它们
# imported by Alembic
"""
from backend.app.database.base_class import MappedBase
from backend.app.models.sys_api import Api
from backend.app.models.sys_casbin_rule import CasbinRule
from backend.app.models.sys_dept import Dept
from backend.app.models.sys_menu import Menu
from backend.app.models.sys_role import Role
from backend.app.models.sys_user import User
