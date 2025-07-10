#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Body
from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.plugin.sms.schema.sms import SendSmsRequest, SendSmsResponse
from backend.plugin.sms.service.sms_service import sms_service

router = APIRouter()


@router.post("/send", summary="发送短信验证码", dependencies=[DependsJwtAuth])
async def send_sms(request: SendSmsRequest = Body(...)) -> ResponseSchemaModel[SendSmsResponse]:
    """
    发送短信验证码
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
