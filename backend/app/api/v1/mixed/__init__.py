#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1.mixed.config import router as config_router
from backend.app.api.v1.mixed.tests import router as upload_router

router = APIRouter()

router.include_router(config_router)
router.include_router(upload_router)
