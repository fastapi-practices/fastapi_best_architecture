#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request
from fastapi.routing import APIRoute

from backend.app.common.rbac import DependsRBAC
from backend.app.common.response.response_schema import response_base
from backend.app.core.conf import settings

router = APIRouter()


@router.get('/configs', summary='获取系统配置', dependencies=[DependsRBAC])
async def get_sys_config():
    return await response_base.success(
        data={
            'title': settings.TITLE,
            'version': settings.VERSION,
            'description': settings.DESCRIPTION,
            'docs_url': settings.DOCS_URL,
            'redocs_url': settings.REDOCS_URL,
            'openapi_url': settings.OPENAPI_URL,
            'environment': settings.ENVIRONMENT,
            'static_files': settings.STATIC_FILES,
            'uvicorn_host': settings.UVICORN_HOST,
            'uvicorn_port': settings.UVICORN_PORT,
            'uvicorn_reload': settings.UVICORN_RELOAD,
            'db_host': settings.DB_HOST,
            'db_port': settings.DB_PORT,
            'db_user': settings.DB_USER,
            'db_database': settings.DB_DATABASE,
            'db_charset': settings.DB_CHARSET,
            'redis_host': settings.REDIS_HOST,
            'redis_port': settings.REDIS_PORT,
            'redis_database': settings.REDIS_DATABASE,
            'redis_timeout': settings.REDIS_TIMEOUT,
            'aps_redis_host': settings.APS_REDIS_HOST,
            'aps_redis_port': settings.APS_REDIS_PORT,
            'aps_redis_database': settings.APS_REDIS_DATABASE,
            'aps_redis_timeout': settings.APS_REDIS_TIMEOUT,
            'aps_coalesce': settings.APS_COALESCE,
            'aps_max_instances': settings.APS_MAX_INSTANCES,
            'aps_misfire_grace_time': settings.APS_MISFIRE_GRACE_TIME,
            'token_algorithm': settings.TOKEN_ALGORITHM,
            'token_expire_seconds': settings.TOKEN_EXPIRE_SECONDS,
            'token_swagger_url': settings.TOKEN_URL_SWAGGER,
            'access_log_filename': settings.LOG_STDOUT_FILENAME,
            'error_log_filename': settings.LOG_STDERR_FILENAME,
            'middleware_cors': settings.MIDDLEWARE_CORS,
            'middleware_gzip': settings.MIDDLEWARE_GZIP,
            'middleware_access': settings.MIDDLEWARE_ACCESS,
        }
    )


@router.get('/routers', summary='获取所有路由', dependencies=[DependsRBAC])
async def get_all_route(request: Request):
    data = []
    for route in request.app.routes:
        if isinstance(route, APIRoute):
            data.append(
                {
                    'path': route.path,
                    'name': route.name,
                    'summary': route.summary,
                    'methods': route.methods,
                    'dependencies': route.dependencies,
                }
            )
    return await response_base.success(data={'route_list': data})
