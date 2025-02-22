#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from contextlib import asynccontextmanager

import socketio

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import Depends, FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import add_pagination
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.staticfiles import StaticFiles

from backend.common.exception.exception_handler import register_exception
from backend.common.log import set_custom_logfile, setup_logging
from backend.core.conf import settings
from backend.core.path_conf import STATIC_DIR, UPLOAD_DIR
from backend.database.db import create_table
from backend.database.redis import redis_client
from backend.middleware.jwt_auth_middleware import JwtAuthMiddleware
from backend.middleware.opera_log_middleware import OperaLogMiddleware
from backend.middleware.state_middleware import StateMiddleware
from backend.plugin.tools import plugin_router_inject
from backend.utils.demo_site import demo_site
from backend.utils.health_check import ensure_unique_route_names, http_limit_callback
from backend.utils.openapi import simplify_operation_ids
from backend.utils.serializers import MsgSpecJSONResponse


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    启动初始化

    :return:
    """
    # 创建数据库表
    await create_table()
    # 连接 redis
    await redis_client.open()
    # 初始化 limiter
    await FastAPILimiter.init(
        redis=redis_client,
        prefix=settings.REQUEST_LIMITER_REDIS_PREFIX,
        http_callback=http_limit_callback,
    )

    yield

    # 关闭 redis 连接
    await redis_client.close()
    # 关闭 limiter
    await FastAPILimiter.close()


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.FASTAPI_TITLE,
        version=settings.FASTAPI_VERSION,
        description=settings.FASTAPI_DESCRIPTION,
        docs_url=settings.FASTAPI_DOCS_URL,
        redoc_url=settings.FASTAPI_REDOC_URL,
        openapi_url=settings.FASTAPI_OPENAPI_URL,
        default_response_class=MsgSpecJSONResponse,
        lifespan=register_init,
    )

    # socketio
    register_socket_app(app)

    # 日志
    register_logger()

    # 静态文件
    register_static_file(app)

    # 中间件
    register_middleware(app)

    # 路由
    register_router(app)

    # 分页
    register_page(app)

    # 全局异常处理
    register_exception(app)

    return app


def register_logger() -> None:
    """
    系统日志

    :return:
    """
    setup_logging()
    set_custom_logfile()


def register_static_file(app: FastAPI):
    """
    静态资源服务，生产应使用 nginx 代理静态资源服务

    :param app:
    :return:
    """
    # 上传静态资源
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    app.mount('/static/upload', StaticFiles(directory=UPLOAD_DIR), name='upload')
    # 固有静态资源
    if settings.FASTAPI_STATIC_FILES:
        app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


def register_middleware(app: FastAPI):
    """
    中间件，执行顺序从下往上

    :param app:
    :return:
    """
    # Opera log (required)
    app.add_middleware(OperaLogMiddleware)
    # JWT auth (required)
    app.add_middleware(
        AuthenticationMiddleware, backend=JwtAuthMiddleware(), on_error=JwtAuthMiddleware.auth_exception_handler
    )
    # Access log
    if settings.MIDDLEWARE_ACCESS:
        from backend.middleware.access_middleware import AccessMiddleware

        app.add_middleware(AccessMiddleware)
    # State
    app.add_middleware(StateMiddleware)
    # Trace ID (required)
    app.add_middleware(CorrelationIdMiddleware, validator=False)
    # CORS: Always at the end
    if settings.MIDDLEWARE_CORS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
            expose_headers=settings.CORS_EXPOSE_HEADERS,
        )


def register_router(app: FastAPI):
    """
    路由

    :param app: FastAPI
    :return:
    """
    dependencies = [Depends(demo_site)] if settings.DEMO_MODE else None

    # API
    plugin_router_inject()

    from backend.app.router import router  # 必须在插件路由注入后导入

    app.include_router(router, dependencies=dependencies)

    # Extra
    ensure_unique_route_names(app)
    simplify_operation_ids(app)


def register_page(app: FastAPI):
    """
    分页查询

    :param app:
    :return:
    """
    add_pagination(app)


def register_socket_app(app: FastAPI):
    """
    socket 应用

    :param app:
    :return:
    """
    from backend.common.socketio.server import sio

    socket_app = socketio.ASGIApp(
        socketio_server=sio,
        other_asgi_app=app,
        # 切勿删除此配置：https://github.com/pyropy/fastapi-socketio/issues/51
        socketio_path='/ws/socket.io',
    )
    app.mount('/ws', socket_app)
