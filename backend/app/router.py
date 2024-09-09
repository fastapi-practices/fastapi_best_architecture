#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.admin.api.router import v1 as admin_v1
from backend.app.generator.api.router import v1 as generator_v1
from backend.app.task.api.router import v1 as task_v1
from backend.core.conf import settings

route = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

route.include_router(admin_v1)
route.include_router(generator_v1)
route.include_router(task_v1)
