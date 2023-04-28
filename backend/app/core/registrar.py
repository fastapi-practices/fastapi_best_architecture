#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_pagination import add_pagination

from backend.app.api.routers import v1
from backend.app.common.exception.exception_handler import register_exception
from backend.app.common.redis import redis_client
from backend.app.common.task import scheduler
from backend.app.core.conf import settings
from backend.app.database.db_mysql import create_table
from backend.app.middleware.access_middle import AccessMiddleware


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    启动初始化

    :return:
    """
    # 创建数据库表
    await create_table()
    # 连接redis
    await redis_client.open()
    # 启动定时任务
    scheduler.start()

    yield

    # 关闭redis连接
    await redis_client.close()
    # 关闭定时任务
    scheduler.shutdown()


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        lifespan=register_init,
    )

    if settings.STATIC_FILES:
        # 注册静态文件
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


def register_static_file(app: FastAPI):
    """
    静态文件交互开发模式, 生产使用 nginx 静态资源服务

    :param app:
    :return:
    """
    import os
    from fastapi.staticfiles import StaticFiles

    if not os.path.exists('./static'):
        os.mkdir('./static')
    app.mount('/static', StaticFiles(directory='static'), name='static')


def register_middleware(app: FastAPI):
    # CORS
    if settings.MIDDLEWARE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
    # Gzip
    if settings.MIDDLEWARE_GZIP:
        app.add_middleware(GZipMiddleware)
    # Api access logs
    if settings.MIDDLEWARE_ACCESS:
        app.add_middleware(AccessMiddleware)


def register_router(app: FastAPI):
    """
    路由

    :param app: FastAPI
    :return:
    """
    app.include_router(v1)


def register_page(app: FastAPI):
    """
    分页查询

    :param app:
    :return:
    """
    add_pagination(app)
