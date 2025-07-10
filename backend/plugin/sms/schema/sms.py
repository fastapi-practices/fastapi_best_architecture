#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Optional
from pydantic import BaseModel, Field


class SendSmsRequest(BaseModel):
    """发送短信请求模型"""
    phone_numbers: List[str] = Field(..., description="手机号码列表，采用E.164标准，格式为+[国家或地区码][手机号]")
    template_id: str = Field(..., description="模板ID，必须填写已审核通过的模板ID")
    template_params: List[str] = Field([], description="模板参数，若无模板参数，则设置为空数组")
    sign_name: str = Field(..., description="短信签名内容，使用UTF-8编码，必须填写已审核通过的签名，比如：中国移动")
    sms_sdk_app_id: str = Field(..., description="短信SdkAppId，在短信控制台添加应用后生成的实际SdkAppId")
    extend_code: Optional[str] = Field(None, description="短信码号扩展号，默认未开通")
    session_context: Optional[str] = Field(None, description="用户的session内容，可以携带用户侧ID等上下文信息")
    sender_id: Optional[str] = Field(None, description="国内短信无需填写该项；国际/港澳台短信已申请独立SenderId需要填写该字段")


class SendStatusItem(BaseModel):
    """短信发送状态项"""
    serial_no: str = Field(..., description="本次发送标识ID")
    phone_number: str = Field(..., description="手机号码")
    fee: int = Field(..., description="计费条数")
    session_context: Optional[str] = Field(None, description="用户的session内容")
    code: str = Field(..., description="状态码，Ok表示成功")
    message: str = Field(..., description="状态描述")
    iso_code: Optional[str] = Field(None, description="国家或地区码")


class SendSmsResponse(BaseModel):
    """发送短信响应模型"""
    send_status_set: List[SendStatusItem] = Field(..., description="短信发送状态列表")
    request_id: str = Field(..., description="请求ID") 