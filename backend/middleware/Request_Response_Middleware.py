# !/usr/bin/python3
# -*- coding: utf-8 -*-

from time import perf_counter
from typing import Any, Dict
from urllib.parse import urlencode

import shortuuid

from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from user_agents import parse

from backend.common.log import log
from backend.utils.json_control import dict_to_json_ensure_ascii, is_dict, json_to_dict


class LogHandler:
    @staticmethod
    async def add_log_record(
        request: Request, event_type: str | None = None, msg: Dict[str, Any] | None = None, remarks: str | None = None
    ):
        """添加日志记录"""
        if msg is None:
            msg = {}
        if hasattr(request.state, 'traceid'):
            trace_links_index = request.state.trace_links_index = getattr(request.state, 'trace_links_index', 0) + 1
            log_info = {
                'traceid': getattr(request.state, 'traceid'),
                'trace_index': trace_links_index,
                'event_type': event_type,
                'msg': msg,
                'remarks': remarks,
            }
            if not remarks:
                log_info.pop('remarks')
            if not msg:
                log_info.pop('msg')
            try:
                log_msg = dict_to_json_ensure_ascii(log_info) if is_dict(log_info) else log_info
                log.info(f'执行的 TRACK: {log_msg}')
            except (TypeError, ValueError) as e:
                log.error(f"{getattr(request.state, 'traceid')}：索引：{trace_links_index}：日志信息写入异常: {e}")

    @staticmethod
    async def start_log_record(request: Request, newness_access_heads_keys: list):
        """初始化请求日志记录"""
        path_info = request.url.path
        if path_info not in ['/favicon.ico'] and 'websocket' not in path_info:
            if request.method != 'OPTIONS':
                request.state.trace_links_index = 0
                request.state.traceid = shortuuid.uuid()
                request.state.start_time = perf_counter()
                ip, method, url = request.client.host, request.method, request.url.path

                body_form = None
                body_json = None
                body_bytes = await request.body()

                content_type = request.headers.get('Content-Type', '')

                if 'application/x-www-form-urlencoded' in content_type or 'multipart/form-data' in content_type:
                    try:
                        form_data = await request.form()
                        body_form = {key: value for key, value in form_data.multi_items()}
                        body_bytes = urlencode(body_form).encode('utf-8')
                    except ValueError:
                        body_form = None

                elif 'application/json' in content_type:
                    if body_bytes:
                        try:
                            body_json = json_to_dict(body_bytes.decode('utf-8'))
                        except ValueError:
                            body_json = body_bytes.decode('gb2312', errors='ignore')

                user_agent = parse(request.headers.get('user-agent', 'unknown'))

                log_msg = {
                    'headers': [request.headers.get(i, '') for i in newness_access_heads_keys]
                    if newness_access_heads_keys
                    else None,
                    'user_agent': {
                        'os': f'{user_agent.os.family} {user_agent.os.version_string}',
                        'browser': f'{user_agent.browser.family} {user_agent.browser.version_string}',
                        'device': {
                            'family': user_agent.device.family,
                            'brand': user_agent.device.brand,
                            'model': user_agent.device.model,
                        },
                    },
                    'url': url,
                    'method': method,
                    'ip': ip,
                    'params': {
                        'query_params': dict(request.query_params),
                        'path_params': request.path_params,
                        'form': body_form,
                        'body': body_json,
                    },
                }

                if not log_msg['headers']:
                    log_msg.pop('headers')

                if not log_msg['params']['query_params']:
                    log_msg['params'].pop('query_params')
                if not log_msg['params']['path_params']:
                    log_msg['params'].pop('path_params')
                if not log_msg['params']['form']:
                    log_msg['params'].pop('form')
                if not log_msg['params']['body']:
                    log_msg['params'].pop('body')

                await LogHandler.add_log_record(request, event_type='request', msg=log_msg)

    @staticmethod
    async def end_log_record(request: Request, response: Response):
        """结束请求日志记录"""
        if isinstance(response, dict):
            response = JSONResponse(content=response)

        # 处理 media_type 为 None 的情况
        if response.media_type is None:
            response.media_type = 'application/json'  # 默认类型

        if response.media_type and 'image' not in response.media_type and hasattr(request.state, 'traceid'):
            start_time = getattr(request.state, 'start_time', perf_counter())
            end_time = f'{(perf_counter() - start_time) * 1000:.2f}ms'
            rsp = None
            if hasattr(response, 'body') and response.body:
                try:
                    rsp = response.body.decode('utf-8')
                except UnicodeDecodeError as e:
                    log.error(f'响应体解码失败: {e}')
            log_msg = {
                'status_code': response.status_code,
                'cost_time': end_time,
                'response': json_to_dict(rsp) if rsp else None,
            }
            await LogHandler.add_log_record(request, event_type='response', msg=log_msg)
