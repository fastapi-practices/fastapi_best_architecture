import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.common.context import ctx
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
        path = request.url.path if not request.url.query else request.url.path + '/' + request.url.query

        if request.method != 'OPTIONS':
            log.debug(f'--> 请求开始[{path}]')

        perf_time = time.perf_counter()
        ctx.perf_time = perf_time

        start_time = timezone.now()
        ctx.start_time = start_time

        response = await call_next(request)

        if request.method != 'OPTIONS':
            log.debug('<-- 请求结束')

            log.info(
                f'{request.client.host: <15} | {request.method: <8} | {response.status_code: <6} | '
                f'{path} | {(time.perf_counter() - perf_time) * 1000:.3f}ms',
            )

        return response
