#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.admin.api.router import v1 as admin_v1
from backend.app.task.api.router import v1 as task_v1
from backend.core.conf import settings

route = APIRouter(prefix=settings.API_V1_STR)

route.include_router(admin_v1)
route.include_router(task_v1)
