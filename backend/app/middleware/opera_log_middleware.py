#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from fastapi import UploadFile
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.types import ASGIApp, Scope, Receive, Send
from user_agents import parse

from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.schemas.opera_log import CreateOperaLog
from backend.app.services.opera_log_service import OperaLogService
from backend.app.utils import request_parse
from backend.app.utils.encrypt import AESCipher


class OperaLogMiddleware:
    """操作日志中间件"""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        request = Request(scope=scope, receive=receive)

        # 排除记录白名单
        path = request.url.path
        if path in settings.OPERA_LOG_EXCLUDE:
            await self.app(scope, receive, send)
            return

        # 请求信息解析
        ip = await request_parse.get_request_ip(request)
        user_agent = request.headers.get('User-Agent')
        user_agent_parsed = parse(user_agent)
        os = user_agent_parsed.get_os()
        browser = user_agent_parsed.get_browser()
        if settings.LOCATION_PARSE == 'online':
            location = await request_parse.get_location_online(ip, user_agent)
        elif settings.LOCATION_PARSE == 'offline':
            location = await request_parse.get_location_offline(ip)
        else:
            location = '未知'
        try:
            # 此信息依赖于 jwt 中间件
            username = request.user.username
        except AttributeError:
            username = None
        method = request.method
        args = dict(request.query_params)
        form_data = await request.form()
        if len(form_data) > 0:
            args.update({k: v.filename if isinstance(v, UploadFile) else v for k, v in form_data.items()})
        else:
            body_data = await request.body()
            if body_data:
                json_data = await request.json()
                args.update(json_data)

        # 设置附加请求信息
        request.state.ip = ip
        request.state.location = location
        request.state.os = os
        request.state.browser = browser

        # 预置响应信息
        code: int = 200
        msg: str = 'Success'
        status: bool = True
        err: Any = None

        # 执行请求
        start_time = datetime.now()
        try:
            # 详见 https://github.com/tiangolo/fastapi/discussions/8385#discussioncomment-6117967
            async def wrapped_rcv_gen():
                async for _ in request.stream():
                    yield {'type': 'http.request', 'body': await request.body()}
                    async for message in request.receive:  # type: ignore
                        # assert message['type'] == 'http.response.body'
                        # body = message.get('body', b'')
                        # if body:
                        #     yield body
                        yield message
            wrapped_rcv = wrapped_rcv_gen().__anext__
            await self.app(request.scope, wrapped_rcv, send)
        except Exception as e:
            log.exception(e)
            code = getattr(e, 'code', 500)
            msg = getattr(e, 'msg', str(e) or 'Internal Server Error')
            status = False
            err = e
        end_time = datetime.now()
        summary = request.scope.get('route').summary
        title = summary if summary != '' else request.scope.get('route').summary
        args.update(request.path_params)
        if len(args) > 0:
            if settings.OPERA_LOG_ENCRYPT:
                for key in args.keys():
                    if key in settings.OPERA_LOG_ENCRYPT_INCLUDE:
                        args[key] = (
                            AESCipher(settings.OPERA_ENCRYPT_SECRET_KEY).encrypt(bytes(args[key], encoding='utf-8'))
                        ).hex()
        args = args if len(args) > 0 else None
        cost_time = (end_time - start_time).total_seconds() * 1000.0

        # 日志创建
        opera_log_in = CreateOperaLog(
            username=username,
            method=method,
            title=title,
            path=path,
            ipaddr=ip,
            location=location,
            os=os,
            browser=browser,
            args=args,
            status=status,
            code=code,
            msg=msg,
            cost_time=cost_time,
            opera_time=start_time,
        )
        back = BackgroundTask(OperaLogService.create, obj_in=opera_log_in)
        await back()

        # 错误抛出
        if err:
            raise err from None
