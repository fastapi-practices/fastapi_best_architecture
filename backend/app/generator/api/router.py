#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.generator.api.v1.gen import router as gen_router

v1 = APIRouter()

v1.include_router(gen_router, prefix='/gen', tags=['代码生成'])
