#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from backend.app.common.log import log


class AccessMiddleware(BaseHTTPMiddleware):
    """
    记录请求日志
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = datetime.now()
        response = await call_next(request)
        end_time = datetime.now()
        log.info(f'{response.status_code} {request.client.host} {request.method} {request.url} {end_time - start_time}')
        return response
