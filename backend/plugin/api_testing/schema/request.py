#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
请求相关模型
"""
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from backend.plugin.api_testing.utils.http_client import RequestOptions


class ApiRequestSchema(BaseModel):
    """API请求模型"""
    url: str = Field(..., description="请求URL")
    method: str = Field(..., description="请求方法", examples=["GET", "POST", "PUT", "DELETE"])
    headers: Optional[Dict[str, str]] = Field(None, description="请求头")
    params: Optional[Dict[str, Any]] = Field(None, description="查询参数")
    data: Optional[Dict[str, Any]] = Field(None, description="表单数据")
    json_data: Optional[Dict[str, Any]] = Field(None, description="JSON数据")
    files: Optional[Dict[str, str]] = Field(None, description="上传文件，值为文件路径")
    auth: Optional[List[str]] = Field(None, description="认证信息[用户名, 密码]")
    options: Optional[RequestOptions] = Field(None, description="请求选项")


class ApiResponseSchema(BaseModel):
    """API响应模型"""
    url: str = Field(..., description="请求URL")
    method: str = Field(..., description="请求方法")
    status_code: int = Field(..., description="状态码")
    elapsed_time: float = Field(..., description="请求耗时(毫秒)")
    headers: Dict[str, str] = Field(..., description="响应头")
    cookies: Dict[str, str] = Field(..., description="响应cookies")
    content: str = Field(..., description="原始响应内容")
    text: str = Field(..., description="文本形式的响应")
    json_data: Optional[Dict[str, Any]] = Field(None, description="JSON形式的响应")
    error: Optional[str] = Field(None, description="错误信息")


class TestCaseRequest(BaseModel):
    """测试用例创建请求"""
    name: str = Field(..., description="用例名称")
    project_id: int = Field(..., description="所属项目ID")
    description: Optional[str] = Field(None, description="用例描述")
    pre_script: Optional[str] = Field(None, description="前置脚本")
    post_script: Optional[str] = Field(None, description="后置脚本")


class TestCaseResponse(BaseModel):
    """测试用例响应"""
    id: int
    name: str
    project_id: int
    description: Optional[str] = None
    pre_script: Optional[str] = None
    post_script: Optional[str] = None
    status: int
    create_time: str
    update_time: str


class TestStepRequest(BaseModel):
    """测试步骤创建请求"""
    name: str = Field(..., description="步骤名称")
    test_case_id: int = Field(..., description="所属用例ID")
    url: str = Field(..., description="请求URL")
    method: str = Field(..., description="请求方法")
    headers: Optional[Dict[str, str]] = Field(None, description="请求头")
    params: Optional[Dict[str, Any]] = Field(None, description="查询参数")
    body: Optional[Dict[str, Any]] = Field(None, description="请求体")
    files: Optional[Dict[str, str]] = Field(None, description="上传文件")
    auth: Optional[Dict[str, str]] = Field(None, description="认证信息")
    extract: Optional[Dict[str, str]] = Field(None, description="提取变量")
    validations: Optional[List[Dict[str, Any]]] = Field(None, description="断言列表")
    sql_queries: Optional[List[Dict[str, Any]]] = Field(None, description="SQL查询列表")
    timeout: int = Field(30, description="超时时间(秒)")
    retry: int = Field(0, description="重试次数")
    retry_interval: int = Field(1, description="重试间隔(秒)")
    order: int = Field(..., description="步骤顺序")


class TestStepResponse(BaseModel):
    """测试步骤响应"""
    id: int
    name: str
    test_case_id: int
    url: str
    method: str
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None
    files: Optional[Dict[str, str]] = None
    auth: Optional[Dict[str, str]] = None
    extract: Optional[Dict[str, str]] = None
    validations: Optional[List[Dict[str, Any]]] = None
    sql_queries: Optional[List[Dict[str, Any]]] = None
    timeout: int
    retry: int
    retry_interval: int
    order: int
    status: int
    create_time: str
    update_time: str