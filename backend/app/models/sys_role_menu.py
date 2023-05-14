#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, ForeignKey, INT, Integer

from backend.app.database.base_class import MappedBase

sys_role_menu = Table(
    'sys_role_menu',
    MappedBase.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column('role_id', Integer, ForeignKey('sys_role.role_id', ondelete='CASCADE'), primary_key=True, comment='角色ID'),
    Column('menu_id', Integer, ForeignKey('sys_menu.menu_id', ondelete='CASCADE'), primary_key=True, comment='菜单ID'),
)
