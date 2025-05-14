#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import INT, Column, ForeignKey, Integer, Table

from backend.common.model import MappedBase

sys_user_role = Table(
    'sys_user_role',
    MappedBase.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='PRIMARY KEY ID'),
    Column('user_id', Integer, ForeignKey('sys_user.id', ondelete='CASCADE'), primary_key=True, comment='USER ID'),
    Column('role_id', Integer, ForeignKey('sys_role.id', ondelete='CASCADE'), primary_key=True, comment='ROLE ID'),
)

sys_role_menu = Table(
    'sys_role_menu',
    MappedBase.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='PRIMARY KEY ID'),
    Column('role_id', Integer, ForeignKey('sys_role.id', ondelete='CASCADE'), primary_key=True, comment='ROLE ID'),
    Column('menu_id', Integer, ForeignKey('sys_menu.id', ondelete='CASCADE'), primary_key=True, comment='MENU ID'),
)

sys_role_data_scope = Table(
    'sys_role_data_scope',
    MappedBase.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='PRIMARY ID'),
    Column('role_id', Integer, ForeignKey('sys_role.id', ondelete='CASCADE'), primary_key=True, comment='ROLE ID'),
    Column(
        'data_scope_id',
        Integer,
        ForeignKey('sys_data_scope.id', ondelete='CASCADE'),
        primary_key=True,
        comment='DATA RANGE ID',
    ),
)
