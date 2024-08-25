# !/usr/bin/python3
# -*- coding: utf-8 -*-

import json

from fastapi import Request

from backend.common.log import log


async def request_info(request: Request):
    """
    记录请求信息的中间件函数
    记录请求的HTTP方法和URL，并根据请求的Content-Type记录请求体的内容。

    :param request: FastAPI的请求对象
    :type request: Request
    """
    body = None
    log.debug(f'{request.method} {request.url}')

    try:
        content_type = request.headers.get('Content-Type', '').lower()

        if 'application/json' in content_type:
            try:
                body = await request.json()
                params = dict(request.query_params)
                if body:
                    # 有请求体，记录日志
                    log.info(f'请求的JSON体: {body}')
                if params:
                    # 有查询参数，记录日志
                    log.info(f'查询参数: {params}')
            except json.JSONDecodeError as e:
                # 捕获 JSON 解析错误
                log.error(f'无效的JSON: {e}')
                body = await request.body()
                log.info(f'原始请求体: {body.decode()}')
        else:
            try:
                body = await request.body()
                if len(body) != 0:
                    # 有请求体，记录日志
                    log.info(body.decode())
            except UnicodeDecodeError as e:
                # 捕获解码错误
                log.error(f'Unicode解码错误: {e}')
                log.info(f'原始请求体: {body}')
    except Exception as e:
        # 捕获所有其他异常
        log.error(f'处理请求体时出错: {e}')
