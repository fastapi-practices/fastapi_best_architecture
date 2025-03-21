#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.utils.request_parse import parse_ip_info, parse_user_agent_info


class StateMiddleware(BaseHTTPMiddleware):
    """请求 state 中间件，用于解析和设置请求的附加信息"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        处理请求并设置请求状态信息

        :param request: FastAPI 请求对象
        :param call_next: 下一个中间件或路由处理函数
        :return:
        """
        ip_info = await parse_ip_info(request)
        ua_info = parse_user_agent_info(request)

        # 设置附加请求信息
        request.state.ip = ip_info.ip
        request.state.country = ip_info.country
        request.state.region = ip_info.region
        request.state.city = ip_info.city
        request.state.user_agent = ua_info.user_agent
        request.state.os = ua_info.os
        request.state.browser = ua_info.browser
        request.state.device = ua_info.device

        response = await call_next(request)

        return response
