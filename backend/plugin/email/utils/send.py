from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from anyio import open_file
from jinja2 import Template
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from backend.common.enums import StatusType
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
        async with await open_file(PLUGIN_DIR / 'email' / 'templates' / template, encoding='utf-8') as f:
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
) -> None:
    """
    发送电子邮件

    :param db: 数据库会话
    :param recipients: 邮件接收者
    :param subject: 邮件内容主题
    :param content: 邮件内容
    :param template: 邮件内容模板
    :return:
    """
    # 本地配置
    email_host = settings.EMAIL_HOST
    email_port = settings.EMAIL_PORT
    email_ssl = settings.EMAIL_SSL
    email_username = settings.EMAIL_USERNAME
    email_password = settings.EMAIL_PASSWORD

    # 动态配置
    dynamic_config = None

    def get_config_table(conn: AsyncConnection) -> bool:
        inspector = inspect(conn)
        return inspector.has_table('sys_config', schema=None)

    async with async_engine.begin() as coon:
        exists = await coon.run_sync(get_config_table)
        if exists:
            dynamic_config = await config_dao.get_all(db, 'EMAIL')

    if dynamic_config:
        status_key = 'EMAIL_STATUS'
        host_key = 'EMAIL_HOST'
        port_key = 'EMAIL_PORT'
        ssl_key = 'EMAIL_SSL'
        username_key = 'EMAIL_USERNAME'
        password_key = 'EMAIL_PASSWORD'

        configs = {d['key']: d['value'] for d in select_list_serialize(dynamic_config)}
        if configs.get(status_key):
            if len(dynamic_config) < 6:
                raise errors.NotFoundError(msg='缺少邮件动态配置，请检查系统参数配置-邮件配置')
            email_host = configs.get(host_key)
            email_port = int(configs.get(port_key, 0))
            email_ssl = configs.get(ssl_key, '') == str(StatusType.enable.value)
            email_username = configs.get(username_key)
            email_password = configs.get(password_key)

    try:
        message = await render_message(subject, email_username, content, template)
        smtp_client = SMTP(
            hostname=email_host,
            port=email_port,
            use_tls=email_ssl,
        )
        async with smtp_client:
            await smtp_client.login(email_username, email_password)
            await smtp_client.sendmail(email_username, recipients, message)
    except Exception as e:
        log.error(f'电子邮件发送失败：{e}')
