#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from fastapi import APIRouter

from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.task_demo import router as task_demo_router

v1 = APIRouter(prefix='/v1')

v1.include_router(auth_router, prefix='/users', tags=['用户管理'])

v1.include_router(task_demo_router, prefix='/tasks', tags=['任务管理'])
