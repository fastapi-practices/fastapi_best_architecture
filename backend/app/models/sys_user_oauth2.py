#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import INT, Column, ForeignKey, Integer, Table

from backend.app.models.base import MappedBase

sys_user_oauth2 = Table(
    'sys_user_oauth2',
    MappedBase.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column('user_id', Integer, ForeignKey('sys_user.id', ondelete='CASCADE'), primary_key=True, comment='用户 ID'),
    Column(
        'social_user_id',
        Integer,
        ForeignKey('sys_social_user.id', ondelete='CASCADE'),
        primary_key=True,
        comment='社交用户 ID',
    ),
)
