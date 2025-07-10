# !/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from fastapi import APIRouter, Body
from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.plugin.sms.schema.sms import SendSmsRequest, SendSmsResponse
from backend.plugin.sms.service.sms_service import sms_service
from backend.database.redis import redis_client
from backend.core.conf import settings

router = APIRouter()


@router.post("/send", summary="发送短信验证码", dependencies=[DependsJwtAuth])
async def send_sms(request: SendSmsRequest = Body(...)) -> ResponseSchemaModel[SendSmsResponse]:
    """
    发送短信验证码(调试)
    """
    result = await sms_service.send_sms(
        phone_numbers=request.phone_numbers,
        template_id=request.template_id,
        template_params=request.template_params,
        sign_name=request.sign_name,
        sms_sdk_app_id=request.sms_sdk_app_id,
        extend_code=request.extend_code,
        session_context=request.session_context,
        sender_id=request.sender_id
    )
    return response_base.success(data=result)


@router.post("/send_login_code", summary="发送登录短信验证码")
async def send_login_code(phone: str = Body(..., embed=True)) -> ResponseSchemaModel:
    """
    发送登录短信验证码，生成5位数验证码，存储在Redis中，有效期5分钟
    """
    # 生成5位数随机验证码
    verification_code = ''.join(random.choices('0123456789', k=5))

    # 存储验证码到Redis，设置5分钟过期时间
    await redis_client.set(
        f'{settings.SMS_LOGIN_REDIS_PREFIX}:{phone}',
        verification_code,
        ex=300  # 5分钟 = 300秒
    )

    # 调用短信服务发送验证码
    await sms_service.send_sms(
        phone_numbers=[phone],
        template_id=settings.SMS_LOGIN_TEMPLATE_ID,
        template_params=[verification_code],
        sign_name=settings.SMS_SIGN_NAME,
        sms_sdk_app_id=settings.SMS_SDK_APP_ID
    )
    return response_base.success(data=f"验证码已发送到手机 {phone}")
