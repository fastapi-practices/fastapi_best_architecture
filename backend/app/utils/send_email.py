#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.utils.generate_string import get_uuid

__only_code = get_uuid()

SEND_RESET_PASSWORD_TEXT = f"您的重置密码验证码为：{__only_code}\n为了不影响您正常使用，" \
                           f"请在{int(settings.COOKIES_MAX_AGE / 60)}分钟内完成密码重置"

SEND_EMAIL_LOGIN_TEXT = f"您的登录验证码为：{__only_code}\n" \
                        f"请在{int(settings.EMAIL_LOGIN_CODE_MAX_AGE / 60)}分钟内完成登录"


async def send_verification_code_email(to: str, code: str, text: str = SEND_RESET_PASSWORD_TEXT):
    """
    发送验证码电子邮件

    :param to:
    :param code:
    :param text:
    :return:
    """
    text = text.replace(__only_code, code)
    msg = MIMEMultipart()
    msg['Subject'] = settings.EMAIL_DESCRIPTION
    msg['From'] = settings.EMAIL_USER
    msg.attach(MIMEText(text, _charset='utf-8'))

    # 登录smtp服务器并发送邮件
    try:
        smtp = aiosmtplib.SMTP(hostname=settings.EMAIL_SERVER, port=settings.EMAIL_PORT, use_tls=settings.EMAIL_SSL)
        async with smtp:
            await smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            await smtp.sendmail(msg['From'], to, msg.as_string())
            await smtp.quit()
    except Exception as e:
        log.error('邮件发送失败 {}', e)
        raise Exception('邮件发送失败 {}'.format(e))
