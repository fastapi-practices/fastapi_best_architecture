import asyncio
import functools
import time

from collections.abc import Callable
from math import ceil
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.routing import APIRoute

from backend.common.exception import errors
from backend.common.log import log
from backend.common.response.response_code import StandardResponseCode


def ensure_unique_route_names(app: FastAPI) -> None:
    """
    检查路由名称是否唯一

    :param app: FastAPI 应用实例
    :return:
    """
    temp_routes = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            if route.name in temp_routes:
                raise ValueError(f'Non-unique route name: {route.name}')
            temp_routes.add(route.name)


async def http_limit_callback(request: Request, response: Response, expire: int) -> None:  # noqa: RUF029
    """
    请求限制时的默认回调函数

    :param request: FastAPI 请求对象
    :param response: FastAPI 响应对象
    :param expire: 剩余毫秒数
    :return:
    """
    expires = ceil(expire / 1000)
    raise errors.HTTPError(
        code=StandardResponseCode.HTTP_429,
        msg='请求过于频繁，请稍后重试',
        headers={'Retry-After': str(expires)},
    )


def timer(func) -> Callable:  # noqa: ANN001
    """函数耗时计时装饰器"""

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed_seconds = time.perf_counter() - start_time
        _log_time(func, elapsed_seconds)
        return result

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_seconds = time.perf_counter() - start_time
        _log_time(func, elapsed_seconds)
        return result

    def _log_time(func, elapsed: float) -> None:  # noqa: ANN001
        # 智能选择单位（秒、毫秒、微秒、纳秒）
        if elapsed >= 1:
            unit, factor = 's', 1
        else:
            unit, factor = 'ms', 1e3

        log.info(f'{func.__module__}.{func.__name__} | {elapsed * factor:.3f} {unit}')

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
