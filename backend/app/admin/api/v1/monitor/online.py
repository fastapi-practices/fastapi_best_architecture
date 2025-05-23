#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.admin.schema.token import GetTokenDetail
from backend.common.enums import StatusType
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth, jwt_decode, revoke_token, superuser_verify
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.core.conf import settings
from backend.database.redis import redis_client

router = APIRouter()


@router.get('', summary='获取在线用户', dependencies=[DependsJwtAuth])
async def get_online(
    username: Annotated[str | None, Query(description='用户名')] = None,
) -> ResponseSchemaModel[list[GetTokenDetail]]:
    token_keys = await redis_client.keys(f'{settings.TOKEN_REDIS_PREFIX}:*')
    online_clients = await redis_client.smembers(settings.TOKEN_ONLINE_REDIS_PREFIX)
    data: list[GetTokenDetail] = []

    def append_token_detail() -> None:
        data.append(
            token_detail.model_copy(
                update={
                    'username': extra_info.get('username', '未知'),
                    'nickname': extra_info.get('nickname', '未知'),
                    'ip': extra_info.get('ip', '未知'),
                    'os': extra_info.get('os', '未知'),
                    'browser': extra_info.get('browser', '未知'),
                    'device': extra_info.get('device', '未知'),
                    'last_login_time': extra_info.get('last_login_time', '未知'),
                }
            )
        )

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
            status=StatusType.enable if session_uuid in online_clients else StatusType.disable,
            last_login_time='未知',
            expire_time=token_payload.expire_time,
        )
        extra_info = await redis_client.get(f'{settings.TOKEN_EXTRA_INFO_REDIS_PREFIX}:{session_uuid}')
        if extra_info:
            extra_info = json.loads(extra_info)
            # 排除 swagger 登录生成的 token
            if extra_info.get('swagger') is None:
                if username is not None:
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
async def kick_out(
    request: Request,
    pk: Annotated[int, Path(description='用户 ID')],
    session_uuid: Annotated[str, Query(description='会话 UUID')],
) -> ResponseModel:
    superuser_verify(request)
    await revoke_token(str(pk), session_uuid)
    return response_base.success()
