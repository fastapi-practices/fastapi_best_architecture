#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.admin.schema.token import GetTokenDetail, KickOutToken
from backend.common.enums import StatusType
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth, jwt_decode, superuser_verify
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.core.conf import settings
from backend.database.redis import redis_client

router = APIRouter()


@router.get('', summary='获取令牌列表', dependencies=[DependsJwtAuth])
async def get_tokens(username: Annotated[str | None, Query()] = None) -> ResponseSchemaModel[list[GetTokenDetail]]:
    token_keys = await redis_client.keys(f'{settings.TOKEN_REDIS_PREFIX}:*')
    token_online = await redis_client.smembers(settings.TOKEN_ONLINE_REDIS_PREFIX)
    data = []
    for key in token_keys:
        token = await redis_client.get(key)
        token_payload = jwt_decode(token)
        session_uuid = token_payload.session_uuid
        token_detail = GetTokenDetail(
            id=token_payload.id,
            session_uuid=session_uuid,
            username='未知',
            nickname='未知',
            ip='未知',
            os='未知',
            browser='未知',
            device='未知',
            status=StatusType.disable if session_uuid not in token_online else StatusType.enable,
            last_login_time='未知',
            expire_time=token_payload.expire_time,
        )
        extra_info = await redis_client.get(f'{settings.TOKEN_EXTRA_INFO_REDIS_PREFIX}:{session_uuid}')
        if extra_info:

            def append_token_detail():
                data.append(
                    token_detail.model_copy(
                        update={
                            'username': extra_info.get('username'),
                            'nickname': extra_info.get('nickname'),
                            'ip': extra_info.get('ip'),
                            'os': extra_info.get('os'),
                            'browser': extra_info.get('browser'),
                            'device': extra_info.get('device'),
                            'last_login_time': extra_info.get('last_login_time'),
                        }
                    )
                )

            extra_info = json.loads(extra_info)
            if extra_info.get('login_type') != 'swagger':
                if username:
                    if username == extra_info.get('username'):
                        append_token_detail()
                else:
                    append_token_detail()
        else:
            data.append(token_detail)
    return response_base.success(data=data)


@router.delete(
    '/{pk}',
    summary='踢下线',
    dependencies=[
        Depends(RequestPermission('sys:token:kick')),
        DependsRBAC,
    ],
)
async def kick_out(request: Request, pk: Annotated[int, Path(...)], session_uuid: KickOutToken) -> ResponseModel:
    superuser_verify(request)
    await redis_client.delete(f'{settings.TOKEN_REDIS_PREFIX}:{pk}:{session_uuid}')
    return response_base.success()
