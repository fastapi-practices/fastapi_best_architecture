#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.task.api.v1.task import router as task_router

v1 = APIRouter()

v1.include_router(task_router, prefix='/tasks', tags=['任务管理'])
