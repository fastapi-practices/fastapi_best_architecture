#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiofiles

from aiosmtplib import SMTP
from jinja2 import Template
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR
from backend.database.db import async_engine
from backend.plugin.config.crud.crud_config import config_dao
from backend.utils.serializers import select_list_serialize
from backend.utils.timezone import timezone


async def render_message(subject: str, from_header: str, content: str | dict, template: str | None) -> bytes:
    """
    渲染邮件内容

    :param subject: 邮件内容主题
    :param from_header: 邮件来源
    :param content: 邮件内容
    :param template: 邮件内容模板
    :return:
    """
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_header
    message['date'] = timezone.now().strftime('%a, %d %b %Y %H:%M:%S %z')

    if template:
        async with aiofiles.open(os.path.join(PLUGIN_DIR, 'email', 'templates', template), 'r', encoding='utf-8') as f:
            html = Template(await f.read(), enable_async=True)
        mail_body = MIMEText(await html.render_async(**content), 'html', 'utf-8')
    else:
        mail_body = MIMEText(content, 'plain', 'utf-8')

    message.attach(mail_body)

    return message.as_bytes()


async def send_email(
    db: AsyncSession,
    recipients: str | list[str],
    subject: str,
    content: str | dict,
    template: str | None = None,
):
    """
    发送电子邮件

    :param db: 数据库会话
    :param recipients: 邮件接收者
    :param subject: 邮件内容主题
    :param content: 邮件内容
    :param template: 邮件内容模板
    :return:
    """
    # 动态配置
    dynamic_email_config = None

    # 检查 config 插件配置
    def get_config_table(conn):
        inspector = inspect(conn)
        return inspector.has_table('sys_config', schema=None)

    async with async_engine.begin() as coon:
        exists = await coon.run_sync(get_config_table)

    if exists:
        dynamic_email_config = await config_dao.get_by_type(db, 'email')

    try:
        # 动态配置发送
        if dynamic_email_config:
            configs = {d['key']: d for d in select_list_serialize(dynamic_email_config)}
            if configs.get('EMAIL_STATUS'):
                if len(dynamic_email_config) < 6:
                    raise errors.NotFoundError(msg='缺少邮件动态配置，请检查系统参数配置-邮件配置')
                smtp_client = SMTP(
                    hostname=configs.get('EMAIL_HOST'),
                    port=configs.get('EMAIL_PORT'),
                    use_tls=configs.get('EMAIL_SSL') == '1',
                )
                message = await render_message(subject, configs.get('EMAIL_USERNAME'), content, template)  # type: ignore
                async with smtp_client:
                    await smtp_client.login(configs.get('EMAIL_USERNAME'), configs.get('EMAIL_PASSWORD'))  # type: ignore
                    await smtp_client.sendmail(configs.get('EMAIL_USERNAME'), recipients, message)  # type: ignore

        # 本地配置发送
        message = await render_message(subject, settings.EMAIL_USERNAME, content, template)
        smtp_client = SMTP(
            hostname=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            use_tls=settings.EMAIL_SSL,
        )
        async with smtp_client:
            await smtp_client.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            await smtp_client.sendmail(settings.EMAIL_USERNAME, recipients, message)
    except Exception as e:
        log.error(f'电子邮件发送失败：{e}')
