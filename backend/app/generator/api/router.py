#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.generator.api.v1.gen import router as gen_router
from backend.app.generator.api.v1.gen_business import router as gen_business_router
from backend.app.generator.api.v1.gen_model import router as gen_model_router

v1 = APIRouter()

v1.include_router(gen_business_router, prefix='/business', tags=['代码生成'])
v1.include_router(gen_model_router, prefix='/model', tags=['代码生成'])
v1.include_router(gen_router, prefix='/gen', tags=['代码生成'])
