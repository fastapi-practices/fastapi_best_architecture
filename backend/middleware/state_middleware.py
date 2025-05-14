#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.utils.request_parse import parse_ip_info, parse_user_agent_info


class StateMiddleware(BaseHTTPMiddleware):
    """request state middle to interpret and set additional information for the request"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Process requests and set up request status information

        :param request: FastAPI
        :param call_text: next intermediate or route processing function
        :return:
        """
        ip_info = await parse_ip_info(request)
        ua_info = parse_user_agent_info(request)

        # Set Additional Request Information
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
