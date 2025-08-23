#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock服务API
"""
from typing import List, Optional

from fastapi import APIRouter, Body, Path, Query
from fastapi.responses import JSONResponse

from backend.common.response.response_schema import response_base, ResponseModel, ResponseSchemaModel
from backend.plugin.api_testing.utils.mock_server import (
    MockProject, MockRule, MockResponse, MockCondition,
    MockServer
)

router = APIRouter()


# Mock项目管理接口
@router.post("/projects", summary="创建Mock项目")
async def create_mock_project(project: MockProject) -> ResponseModel | ResponseSchemaModel:
    """
    创建Mock项目
    """
    success = await MockServer.create_project(project)
    if success:
        return response_base.success(data=project.model_dump())
    else:
        return response_base.fail()


@router.get("/projects/{project_id}", summary="获取Mock项目")
async def get_mock_project(project_id: int = Path(description="项目ID")) -> ResponseModel | ResponseSchemaModel:
    """
    获取Mock项目
    """
    project = await MockServer.get_project(project_id)
    if project:
        return response_base.success(data=project.model_dump())
    else:
        return response_base.fail()


@router.put("/projects/{project_id}", summary="更新Mock项目")
async def update_mock_project(
        project: MockProject,
        project_id: int = Path(description="项目ID")
) -> ResponseModel | ResponseSchemaModel:
    """
    更新Mock项目
    """
    # 确保路径参数和请求体ID一致
    if project.id != project_id:
        return response_base.fail(data="项目ID不匹配")

    success = await MockServer.update_project(project)
    if success:
        return response_base.success(data=project.model_dump())
    else:
        return response_base.fail(data="更新Mock项目失败")


@router.delete("/projects/{project_id}", summary="删除Mock项目")
async def delete_mock_project(project_id: int = Path(description="项目ID")) -> ResponseModel | ResponseSchemaModel:
    """
    删除Mock项目
    """
    success = await MockServer.delete_project(project_id)
    if success:
        return response_base.success(data="删除Mock项目成功")
    else:
        return response_base.fail(data="删除Mock项目失败")


@router.get("/projects", summary="获取所有Mock项目")
async def list_mock_projects() -> ResponseModel | ResponseSchemaModel:
    """
    获取所有Mock项目
    """
    projects = await MockServer.list_projects()
    return response_base.success(data=[project.model_dump() for project in projects])


# Mock规则管理接口
@router.post("/rules", summary="创建Mock规则")
async def create_mock_rule(rule: MockRule) -> ResponseModel | ResponseSchemaModel:
    """
    创建Mock规则
    """
    success = await MockServer.create_rule(rule)
    if success:
        return response_base.success(data=rule.model_dump())
    else:
        return response_base.fail(data="Mock规则创建失败")


@router.get("/rules/{rule_id}", summary="获取Mock规则")
async def get_mock_rule(
        rule_id: str = Path(description="规则ID"),
        project_id: int = Query(description="项目ID")
) -> ResponseModel | ResponseSchemaModel:
    """
    获取Mock规则
    """
    rule = await MockServer.get_rule(rule_id, project_id)
    if rule:
        return response_base.success(data=rule.model_dump())
    else:
        return response_base.fail(data="Mock规则不存在")


@router.put("/rules/{rule_id}", summary="更新Mock规则")
async def update_mock_rule(
        rule: MockRule,
        rule_id: str = Path(description="规则ID"),
        project_id: int = Query(description="项目ID")
) -> ResponseModel | ResponseSchemaModel:
    """
    更新Mock规则
    """
    # 确保路径参数和请求体ID一致
    if rule.id != rule_id or rule.project_id != project_id:
        return response_base.fail(data="规则ID或项目ID不匹配")

    success = await MockServer.update_rule(rule)
    if success:
        return response_base.success(data=rule.model_dump())
    else:
        return response_base.fail(data="更新Mock规则失败")


@router.delete("/rules/{rule_id}", summary="删除Mock规则")
async def delete_mock_rule(
        rule_id: str = Path(description="规则ID"),
        project_id: int = Query(description="项目ID")
) -> ResponseModel | ResponseSchemaModel:
    """
    删除Mock规则
    """
    success = await MockServer.delete_rule(rule_id, project_id)
    if success:
        return response_base.success(data="删除Mock规则成功")
    else:
        return response_base.fail(data="删除Mock规则失败")


@router.get("/rules", summary="获取项目的所有Mock规则")
async def list_mock_rules(project_id: int = Query(..., description="项目ID")) -> ResponseModel | ResponseSchemaModel:
    """
    获取项目的所有Mock规则
    """
    rules = await MockServer.list_rules(project_id)
    return response_base.success(
        data=[rule.model_dump() for rule in rules]
    )


@router.get("/server-info", summary="获取Mock服务信息")
async def get_mock_server_info() -> ResponseModel | ResponseSchemaModel:
    """
    获取Mock服务信息
    """
    info = {
        "app_name": MockServer.app.title,
        "version": "0.1.0",
        "description": "API Testing Mock Server",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
    return response_base.success(data=info, msg="获取Mock服务信息成功")
