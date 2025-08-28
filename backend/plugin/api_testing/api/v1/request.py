#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
接口请求API
"""
from typing import Any, Dict
from fastapi import APIRouter
from backend.plugin.api_testing.schema.request import ApiRequestSchema, ApiResponseSchema
from backend.plugin.api_testing.utils.http_client import send_request
from backend.common.response.response_schema import response_base, ResponseModel, ResponseSchemaModel

router = APIRouter()


@router.post("/send", response_model=ResponseModel, summary="发送API请求")
async def send_api_request(request_data: ApiRequestSchema) -> ResponseModel | ResponseSchemaModel:
    """
    发送API请求接口
    
    发送一个HTTP请求并返回结果
    """
    # 处理文件上传
    files = None
    if request_data.files:
        files = {}
        for field_name, file_path in request_data.files.items():
            try:
                with open(file_path, "rb") as file:
                    files[field_name] = (file_path.split("/")[-1], file.read())
            except Exception as error:
                return response_base.fail()

    # 处理认证信息
    auth = None
    if request_data.auth and len(request_data.auth) >= 2:
        auth = (request_data.auth[0], request_data.auth[1])

    # 发送请求
    try:
        response = await send_request(
            method=request_data.method,
            url=request_data.url,
            params=request_data.params,
            headers=request_data.headers,
            data=request_data.data,
            json_data=request_data.json_data,
            files=files,
            auth=auth,
            options=request_data.options
        )

        # 构建响应
        response_data = ApiResponseSchema(
            url=response.url,
            method=response.method,
            status_code=response.status_code,
            elapsed_time=response.elapsed_time,
            headers=response.headers,
            cookies=response.cookies,
            content=response.content,
            text=response.text,
            json_data=response.json_data,
            error=response.error
        )

        return response_base.success(data=response_data.model_dump())
    except Exception as error:
        # self._handle_exception(error)
        return response_base.fail()
