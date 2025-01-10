#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.generator.api.v1.gen import router as gen_router
from backend.app.generator.api.v1.gen_business import router as gen_business_router
from backend.app.generator.api.v1.gen_model import router as gen_model_router
from backend.core.conf import settings

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/gen', tags=['代码生成'])

v1.include_router(gen_router)
v1.include_router(gen_business_router, prefix='/businesses')
v1.include_router(gen_model_router, prefix='/models')
