#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.jwt import DependsSuperUser
from backend.app.common.response.response_schema import ResponseModel
from backend.app.core.conf import settings

router = APIRouter()


@router.get('', summary='获取系统配置', dependencies=[DependsSuperUser])
async def get_sys_config() -> ResponseModel:
    return ResponseModel(
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
            'db_password': settings.DB_PASSWORD,
            'db_database': settings.DB_DATABASE,
            'db_charset': settings.DB_CHARSET,
            'redis_host': settings.REDIS_HOST,
            'redis_port': settings.REDIS_PORT,
            'redis_password': settings.REDIS_PASSWORD,
            'redis_database': settings.REDIS_DATABASE,
            'redis_timeout': settings.REDIS_TIMEOUT,
            'aps_redis_host': settings.APS_REDIS_HOST,
            'aps_redis_port': settings.APS_REDIS_PORT,
            'aps_redis_password': settings.APS_REDIS_PASSWORD,
            'aps_redis_database': settings.APS_REDIS_DATABASE,
            'aps_redis_timeout': settings.APS_REDIS_TIMEOUT,
            'aps_coalesce': settings.APS_COALESCE,
            'aps_max_instances': settings.APS_MAX_INSTANCES,
            'aps_misfire_grace_time': settings.APS_MISFIRE_GRACE_TIME,
            'token_algorithm': settings.TOKEN_ALGORITHM,
            'token_expire_minutes': settings.TOKEN_EXPIRE_MINUTES,
            'token_url': settings.TOKEN_URL,
            'token_secret_key': settings.TOKEN_SECRET_KEY,
            'log_file_name': settings.LOG_FILE_NAME,
            'middleware_cors': settings.MIDDLEWARE_CORS,
            'middleware_gzip': settings.MIDDLEWARE_GZIP,
            'middleware_access': settings.MIDDLEWARE_ACCESS,
        }
    )
