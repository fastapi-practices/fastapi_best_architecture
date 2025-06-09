#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import INT, Column, ForeignKey, Integer, Table

from backend.common.model import MappedBase

sys_user_role = Table(
    'sys_user_role',
    MappedBase.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column('user_id', Integer, ForeignKey('sys_user.id', ondelete='CASCADE'), primary_key=True, comment='用户ID'),
    Column('role_id', Integer, ForeignKey('sys_role.id', ondelete='CASCADE'), primary_key=True, comment='角色ID'),
)

sys_role_menu = Table(
    'sys_role_menu',
    MappedBase.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column('role_id', Integer, ForeignKey('sys_role.id', ondelete='CASCADE'), primary_key=True, comment='角色ID'),
    Column('menu_id', Integer, ForeignKey('sys_menu.id', ondelete='CASCADE'), primary_key=True, comment='菜单ID'),
)

sys_role_data_scope = Table(
    'sys_role_data_scope',
    MappedBase.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键 ID'),
    Column('role_id', Integer, ForeignKey('sys_role.id', ondelete='CASCADE'), primary_key=True, comment='角色 ID'),
    Column(
        'data_scope_id',
        Integer,
        ForeignKey('sys_data_scope.id', ondelete='CASCADE'),
        primary_key=True,
        comment='数据范围 ID',
    ),
)

sys_data_scope_rule = Table(
    'sys_data_scope_rule',
    MappedBase.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column(
        'data_scope_id',
        Integer,
        ForeignKey('sys_data_scope.id', ondelete='CASCADE'),
        primary_key=True,
        comment='数据范围 ID',
    ),
    Column(
        'data_rule_id',
        Integer,
        ForeignKey('sys_data_rule.id', ondelete='CASCADE'),
        primary_key=True,
        comment='数据规则 ID',
    ),
)
