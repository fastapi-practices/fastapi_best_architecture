#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.admin.schema.token import GetTokenDetail, KickOutToken
from backend.common.enums import StatusType
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth, jwt_decode, revoke_token, superuser_verify
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.core.conf import settings
from backend.database.redis import redis_client

router = APIRouter()


@router.get('', summary='Get token list', dependencies=[DependsJwtAuth])
async def get_tokens(
    username: Annotated[str | None, Query(description='Username')] = None,
) -> ResponseSchemaModel[list[GetTokenDetail]]:
    token_keys = await redis_client.keys(f'{settings.TOKEN_REDIS_PREFIX}:*')
    online_clients = await redis_client.smembers(settings.TOKEN_ONLINE_REDIS_PREFIX)
    data: list[GetTokenDetail] = []

    def append_token_detail() -> None:
        data.append(
            token_detail.model_copy(
                update={
                    'username': extra_info.get('username', 'Unknown'),
                    'nickname': extra_info.get('nickname', 'Unknown'),
                    'ip': extra_info.get('ip', 'Unknown'),
                    'os': extra_info.get('os', 'Unknown'),
                    'browser': extra_info.get('browser', 'Unknown'),
                    'device': extra_info.get('device', 'Unknown'),
                    'last_login_time': extra_info.get('last_login_time', 'Unknown'),
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
            username='Unknown',
            nickname='Unknown',
            ip='Unknown',
            os='Unknown',
            browser='Unknown',
            device='Unknown',
            status=StatusType.enable if session_uuid in online_clients else StatusType.disable,
            last_login_time='Unknown',
            expire_time=token_payload.expire_time,
        )
        extra_info = await redis_client.get(f'{settings.TOKEN_EXTRA_INFO_REDIS_PREFIX}:{session_uuid}')
        if extra_info:
            extra_info = json.loads(extra_info)
            # excludes swagger login generated token
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
    summary='Kick off',
    dependencies=[
        Depends(RequestPermission('sys:token:kick')),
        DependsRBAC,
    ],
)
async def kick_out(
    request: Request, pk: Annotated[int, Path(description='USER ID')], obj: KickOutToken
) -> ResponseModel:
    superuser_verify(request)
    await revoke_token(str(pk), obj.session_uuid)
    return response_base.success()
