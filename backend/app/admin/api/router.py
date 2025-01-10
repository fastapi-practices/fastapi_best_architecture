#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.admin.api.v1.auth import router as auth_router
from backend.app.admin.api.v1.log import router as log_router
from backend.app.admin.api.v1.monitor import router as monitor_router
from backend.app.admin.api.v1.oauth2 import router as oauth2_router
from backend.app.admin.api.v1.sys import router as sys_router
from backend.core.conf import settings

v1 = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

v1.include_router(auth_router)
v1.include_router(oauth2_router)
v1.include_router(sys_router)
v1.include_router(log_router)
v1.include_router(monitor_router)
