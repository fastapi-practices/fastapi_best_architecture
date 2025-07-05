#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.common.log import log
from backend.utils.timezone import timezone


class AccessMiddleware(BaseHTTPMiddleware):
    """访问日志中间件"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        处理请求并记录访问日志

        :param request: FastAPI 请求对象
        :param call_next: 下一个中间件或路由处理函数
        :return:
        """
        log.info(
            f'发送请求：[{request.client.host}] - [{request.method}] - '
            f'[{request.url.path if not request.url.query else request.url.path + "/" + request.url.query}]'
        )

        perf_time = time.perf_counter()
        request.state.perf_time = perf_time

        start_time = timezone.now()
        request.state.start_time = start_time

        response = await call_next(request)

        elapsed = (time.perf_counter() - perf_time) * 1000
        log.info(f'接口耗时：{elapsed:.3f}ms')
        log.info(f'请求结束：{response.status_code}')

        return response
