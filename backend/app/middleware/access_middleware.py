#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime

from fastapi import Request, Response, UploadFile
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware
from user_agents import parse

from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.schemas.opera_log import CreateOperaLog
from backend.app.services.opera_log_service import OperaLogService
from backend.app.utils import request_parse

# TODO: 改为原生ASGI中间件
class OperaLogMiddleware(BaseHTTPMiddleware):
    """操作日志中间件"""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = datetime.now()
        path = request.url.path
        if path in [settings.DOCS_URL, settings.REDOCS_URL, settings.OPENAPI_URL]:
            response = await call_next(request)
            return response
        response = None
        code = 200
        msg = 'Success'
        status = True
        # err = None
        try:
            response = await call_next(request)
        except Exception as e:
            log.exception(e)
            code = getattr(e, 'code', 500)
            msg = getattr(e, 'msg', 'Internal Server Error')
            status = False
            # err = e
        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = None
        method = request.method
        _summary = request.scope.get('route').summary
        title = _summary if _summary != '' else request.scope.get('route').summary
        ip = await request_parse.get_request_ip(request)
        _user_agent = request.headers.get('User-Agent')
        _, _os, _browser = str(parse(_user_agent)).replace(' ', '').split('/')
        if settings.LOCATION_PARSE == 'online':
            location = await request_parse.get_location_online(ip, _user_agent)
        elif settings.LOCATION_PARSE == 'offline':
            location = request_parse.get_location_offline(ip)
        else:
            location = '未知'
        if method == 'GET':
            request_args = str(request.query_params)
        else:
            form_data = await request.form()
            if len(form_data) > 0:
                request_args = json.dumps(
                    {k: v.filename if isinstance(v, UploadFile) else v for k, v in form_data.items()},
                    ensure_ascii=False,
                )
            else:
                json_data = await request.json()
                request_args = json.dumps(json_data, ensure_ascii=False)
        end_time = datetime.now()
        cost_time = (end_time - start_time).total_seconds() / 1000.0
        obj_in = CreateOperaLog(
            username=username,
            method=method,
            title=title,
            path=path,
            ipaddr=ip,
            location=location,
            request=request_args,
            response=None,
            status=status,
            code=code,
            msg=msg,
            cost_time=cost_time,
            opera_time=start_time,
        )
        task = BackgroundTask(OperaLogService.create, obj_in)
        response.background = task
        # if not status:
        #     raise err from None
        request.state.ip = ip
        request.state.location = location
        request.state.os = _os
        request.state.browser = _browser
        return response
