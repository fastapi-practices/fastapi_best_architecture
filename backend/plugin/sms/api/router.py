#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.core.conf import settings
from backend.plugin.sms.api.v1.sms import router as sms_router

# 创建主路由
v1 = APIRouter(prefix=f"{settings.FASTAPI_API_V1_PATH}",tags=["短信服务"])

# 包含v1版本路由
v1.include_router(sms_router,prefix='/sms')