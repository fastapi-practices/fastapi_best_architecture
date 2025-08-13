#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.core.conf import settings
from backend.plugin.email.api.v1.email import router as email_router

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/emails', tags=['电子邮件'])

v1.include_router(email_router)
