#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Request

from backend.app.common.exception.errors import ServerError
from backend.app.core.conf import settings


class RequestPermission:
    def __init__(self, value: str):
        self.value = value

    async def __call__(self, request: Request):
        if settings.PERMISSION_MODE == 'role-menu':
            if not isinstance(self.value, str):
                raise ServerError
            # 附加权限标识
            request.state.permission = self.value
