#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import functools
import time

from math import ceil
from typing import Any, Callable

from fastapi import FastAPI, Request, Response
from fastapi.routing import APIRoute

from backend.common.exception import errors
from backend.common.log import log


def ensure_unique_route_names(app: FastAPI) -> None:
    """
    Check if the route name is unique

    :param app: FastAPI application instance
    :return:
    """
    temp_routes = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            if route.name in temp_routes:
                raise ValueError(f'Non-unique route name: {route.name}')
            temp_routes.add(route.name)


async def http_limit_callback(request: Request, response: Response, expire: int) -> None:
    """
    Default callback function when requesting limit

    :param request: FastAPI
    :param responding objects
    :param expire: ms left
    :return:
    """
    expires = ceil(expire / 1000)
    raise errors.HTTPError(code=429, msg='Please try again later', headers={'Retry-After': str(expires)})


def timer(func) -> Callable:
    """Function Time-timer Decorator"""

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

    def _log_time(func, elapsed: float):
        # Smart selection units (seconds, milliseconds, microseconds, nanoseconds)）
        if elapsed >= 1:
            unit, factor = 's', 1
        else:
            unit, factor = 'ms', 1e3

        log.info(f'{func.__module__}.{func.__name__} | {elapsed * factor:.3f} {unit}')

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
