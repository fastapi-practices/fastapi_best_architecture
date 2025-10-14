from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette_context import context

from backend.utils.request_parse import parse_ip_info, parse_user_agent_info


class StateMiddleware(BaseHTTPMiddleware):
    """请求状态中间件"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        处理请求并设置请求状态信息

        :param request: FastAPI 请求对象
        :param call_next: 下一个中间件或路由处理函数
        :return:
        """
        ip_info = await parse_ip_info(request)
        context['ip'] = ip_info.ip
        context['country'] = ip_info.country
        context['region'] = ip_info.region
        context['city'] = ip_info.city

        ua_info = parse_user_agent_info(request)
        context['user_agent'] = ua_info.user_agent
        context['os'] = ua_info.os
        context['browser'] = ua_info.browser
        context['device'] = ua_info.device

        response = await call_next(request)

        return response
