#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
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
        _, os, browser = str(parse(user_agent)).replace(' ', '').split('/')
        if settings.LOCATION_PARSE == 'online':
            location = await request_parse.get_location_online(ip, user_agent)
        elif settings.LOCATION_PARSE == 'offline':
            location = request_parse.get_location_offline(ip)
        else:
            location = '未知'
        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = None
        method = request.method
        args = dict(request.query_params)
        form_data = await request.form()
        if len(form_data) > 0:
            args = json.dumps(
                args.update({k: v.filename if isinstance(v, UploadFile) else v for k, v in form_data.items()}),
                ensure_ascii=False,
            )
        else:
            body = await request.body()
            if body:
                json_data = await request.json()
                args = json.dumps(args.update(json_data), ensure_ascii=False)
        args = str(args) if len(args) > 0 else None

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
            await self.app(request.scope, request.receive, send)
            log.info('3')
        except Exception as e:
            log.info('4')
            # log.exception(e)
            code = getattr(e, 'code', 500)
            msg = getattr(e, 'msg', 'Internal Server Error')
            status = False
            err = e
        end_time = datetime.now()
        summary = request.scope.get('route').summary
        title = summary if summary != '' else request.scope.get('route').summary
        cost_time = (end_time - start_time).total_seconds() / 1000.0

        # 日志创建
        opera_log_in = CreateOperaLog(
            username=username,
            method=method,
            title=title,
            path=path,
            ipaddr=ip,
            location=location,
            args=args,
            status=status,
            code=code,
            msg=msg,
            cost_time=cost_time,
            opera_time=start_time,
        )
        back = BackgroundTask(OperaLogService.create, opera_log_in)
        await back()

        # 错误抛出
        if err:
            raise err from None
