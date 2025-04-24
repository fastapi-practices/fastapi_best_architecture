#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, INT, Integer, ForeignKey

from backend.common.model import MappedBase

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
