#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# !/usr/bin/python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.common.log import log
from backend.core.conf import settings
from backend.middleware.Request_Response_Middleware import LogHandler
from backend.utils.timezone import timezone


class AccessMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""

    def __init__(self, app: FastAPI, newness_access_heads_keys: list = None):
        super().__init__(app)
        self.newness_access_heads_keys = newness_access_heads_keys

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = timezone.now()
        # 根据 settings.debug 决定是否记录详细日志
        if settings.DEBUG:
            # 开始记录详细的请求日志
            await LogHandler.start_log_record(request, self.newness_access_heads_keys)

        # 继续处理请求
        response = await call_next(request)
        end_time = timezone.now()

        if settings.DEBUG:
            # 结束记录详细的响应日志
            await LogHandler.end_log_record(request, response)

        # 添加 traceid 到响应头
        if hasattr(request.state, 'traceid'):
            response.headers['traceid'] = getattr(request.state, 'traceid')

        # 如果 debug 模式关闭，仍然记录基础的请求日志（可选）
        if not settings.DEBUG:
            log.info(
                f'{request.client.host: <15} | {request.method: <8} | {response.status_code: <6} | '
                f'{request.url.path} | {round((end_time - start_time).total_seconds(), 3) * 1000.0}ms'
            )

        return response
