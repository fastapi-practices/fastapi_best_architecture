#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.core.conf import settings
from backend.plugin.code_generator.api.v1.business import router as business_router
from backend.plugin.code_generator.api.v1.column import router as model_router
from backend.plugin.code_generator.api.v1.gen import router as gen_router

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/gen', tags=['代码生成'])

v1.include_router(gen_router, prefix='/tables')
v1.include_router(business_router, prefix='/businesses')
v1.include_router(model_router, prefix='/models')
