#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
接口请求客户端
基于httpx实现HTTP请求功能
"""
import json
import time
from typing import Any, Dict, List, Optional, Union

import httpx
from fastapi import HTTPException
from pydantic import BaseModel


class RequestOptions(BaseModel):
    """请求选项配置"""
    timeout: int = 30  # 请求超时时间
    verify_ssl: bool = True  # 是否验证SSL证书
    follow_redirects: bool = True  # 是否跟随重定向
    max_redirects: int = 5  # 最大重定向次数
    retry_count: int = 0  # 重试次数
    retry_interval: int = 1  # 重试间隔(秒)


class RequestResult(BaseModel):
    """请求结果模型"""
    url: str
    method: str
    status_code: int
    elapsed_time: float  # 请求耗时(毫秒)
    headers: Dict[str, str]  # 响应头
    cookies: Dict[str, str] = {}  # 响应cookies
    content: str  # 原始响应内容
    text: str  # 文本形式的响应
    json_data: Optional[Dict[str, Any]] = None  # JSON形式的响应
    error: Optional[str] = None  # 错误信息


class HttpClient:
    """HTTP客户端"""
    
    def __init__(self, options: RequestOptions = None):
        """
        初始化HTTP客户端
        
        :param options: 请求选项
        """
        self.options = options or RequestOptions()
        
    async def request(
        self,
        method: str,
        url: str,
        params: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        cookies: Dict[str, str] = None,
        data: Dict[str, Any] = None,
        json_data: Dict[str, Any] = None,
        files: Dict[str, Any] = None,
        auth: tuple = None,
        options: RequestOptions = None
    ) -> RequestResult:
        """
        发送HTTP请求
        
        :param method: 请求方法
        :param url: 请求URL
        :param params: URL查询参数
        :param headers: 请求头
        :param cookies: 请求cookies
        :param data: 表单数据
        :param json_data: JSON数据
        :param files: 上传的文件
        :param auth: 认证信息(用户名, 密码)
        :param options: 请求选项，覆盖默认选项
        :return: 请求结果
        """
        opts = options or self.options
        
        # 准备客户端参数
        client_kwargs = {
            "timeout": opts.timeout,
            "verify": opts.verify_ssl,
            "follow_redirects": opts.follow_redirects,
            "max_redirects": opts.max_redirects
        }
        
        # 准备请求参数
        request_kwargs = {
            "method": method,
            "url": url,
            "params": params,
            "headers": headers,
            "cookies": cookies,
            "data": data,
            "json": json_data,
            "files": files,
            "auth": auth
        }
        
        # 过滤None值
        request_kwargs = {k: v for k, v in request_kwargs.items() if v is not None}
        
        start_time = time.time()
        error = None
        response = None
        retry_count = 0
        
        # 支持请求重试
        while retry_count <= opts.retry_count:
            try:
                async with httpx.AsyncClient(**client_kwargs) as client:
                    response = await client.request(**request_kwargs)
                    break
            except Exception as e:
                error = str(e)
                retry_count += 1
                if retry_count <= opts.retry_count:
                    # 等待重试
                    time.sleep(opts.retry_interval)
                else:
                    break
        
        elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒
        
        if response is None:
            # 请求失败，返回错误信息
            return RequestResult(
                url=url,
                method=method.upper(),
                status_code=0,
                elapsed_time=elapsed_time,
                headers={},
                content="",
                text="",
                error=error
            )
        
        # 尝试解析JSON
        json_result = None
        try:
            if response.headers.get('content-type', '').startswith('application/json'):
                json_result = response.json()
        except Exception:
            pass
            
        # 构建结果
        result = RequestResult(
            url=str(response.url),
            method=method.upper(),
            status_code=response.status_code,
            elapsed_time=elapsed_time,
            headers=dict(response.headers),
            cookies=dict(response.cookies),
            content=response.content.decode('utf-8', errors='replace'),
            text=response.text,
            json_data=json_result
        )
        
        return result


# 创建默认客户端实例
default_client = HttpClient()


async def send_request(
    method: str,
    url: str,
    params: Dict[str, Any] = None,
    headers: Dict[str, str] = None,
    cookies: Dict[str, str] = None,
    data: Dict[str, Any] = None,
    json_data: Dict[str, Any] = None,
    files: Dict[str, Any] = None,
    auth: tuple = None,
    options: RequestOptions = None
) -> RequestResult:
    """
    使用默认客户端发送请求的辅助函数
    
    :param method: 请求方法
    :param url: 请求URL
    :param params: URL查询参数
    :param headers: 请求头
    :param cookies: 请求cookies
    :param data: 表单数据
    :param json_data: JSON数据
    :param files: 上传的文件
    :param auth: 认证信息(用户名, 密码)
    :param options: 请求选项
    :return: 请求结果
    """
    return await default_client.request(
        method=method,
        url=url,
        params=params,
        headers=headers,
        cookies=cookies,
        data=data,
        json_data=json_data,
        files=files,
        auth=auth,
        options=options
    )