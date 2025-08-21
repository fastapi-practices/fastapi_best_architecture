#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Optional
# 导入腾讯云SDK
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.sms.v20210111 import sms_client, models
from backend.common.log import log
from backend.core.conf import settings
from backend.plugin.sms.schema.sms import SendStatusItem, SendSmsResponse


class SmsService:
    """腾讯云短信服务"""

    async def send_sms(
            self,
            phone_numbers: List[str],
            template_id: str,
            template_params: List[str],
            sign_name: str,
            sms_sdk_app_id: str,
            extend_code: Optional[str] = None,
            session_context: Optional[str] = None,
            sender_id: Optional[str] = None
    ) -> SendSmsResponse:
        """
        发送短信
        
        Args:
            phone_numbers: 手机号码列表
            template_id: 模板ID
            template_params: 模板参数列表
            sign_name: 短信签名
            sms_sdk_app_id: 短信应用ID
            extend_code: 扩展码
            session_context: 会话上下文
            sender_id: 国际/港澳台短信发送者ID
            
        Returns:
            SendSmsResponse: 发送结果
        """
        try:
            # 实例化一个认证对象
            cred = credential.Credential(settings.TENCENTCLOUD_SECRET_ID, settings.TENCENTCLOUD_SECRET_KEY)

            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            http_profile = HttpProfile()
            http_profile.endpoint = "sms.tencentcloudapi.com"

            # 实例化一个client选项
            client_profile = ClientProfile()
            client_profile.httpProfile = http_profile

            # 实例化要请求产品的client对象
            client = sms_client.SmsClient(cred, "ap-guangzhou", client_profile)

            # 实例化一个请求对象
            req = models.SendSmsRequest()

            # 设置请求参数
            req.PhoneNumberSet = phone_numbers
            req.SmsSdkAppId = sms_sdk_app_id
            req.SignName = sign_name
            req.TemplateId = template_id
            req.TemplateParamSet = template_params

            if extend_code:
                req.ExtendCode = extend_code
            if session_context:
                req.SessionContext = session_context
            if sender_id:
                req.SenderId = sender_id

            # 发起API请求
            resp = client.SendSms(req)

            # 解析响应结果
            send_status_set = []
            for status in resp.SendStatusSet:
                send_status_set.append(
                    SendStatusItem(
                        serial_no=status.SerialNo,
                        phone_number=status.PhoneNumber,
                        fee=status.Fee,
                        session_context=status.SessionContext,
                        code=status.Code,
                        message=status.Message,
                        iso_code=status.IsoCode
                    )
                )
            log.info(f"腾讯云短信发送成功: {send_status_set}")
            return SendSmsResponse(
                send_status_set=send_status_set,
                request_id=resp.RequestId
            )

        except TencentCloudSDKException as err:
            log.error(f"腾讯云短信发送失败: {err}")
            raise Exception(f"短信发送失败: {err}")
        except Exception as e:
            log.error(f"短信发送异常: {e}")
            raise Exception(f"短信发送异常: {e}")


# 创建服务实例
sms_service = SmsService()
