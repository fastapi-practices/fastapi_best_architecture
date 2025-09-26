#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API项目管理接口
"""
from datetime import datetime
from fastapi import APIRouter, Path, Query
from backend.common.response.response_schema import response_base, ResponseModel, ResponseSchemaModel
from backend.plugin.api_testing.service.project_service import ProjectService
from backend.plugin.api_testing.schema.request import (ProjectCreateRequest, ProjectUpdateRequest, ProjectResponse)

router = APIRouter()


@router.post("", response_model=ResponseModel, summary="创建API项目")
async def create_project(project_data: ProjectCreateRequest) -> ResponseModel | ResponseSchemaModel:
    """
    创建 API 项目
    """
    try:
        project = await ProjectService.create_project(project_data)

        project_response = ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            base_url=project.base_url,
            headers=project.headers,
            variables=project.variables,
            status=project.status,
            created_time=project.created_time.isoformat() if project.created_time else "",
            updated_time=project.updated_time.isoformat() if project.updated_time else ""
        )
        return response_base.success(data=project_response.model_dump())
    except Exception as e:
        return response_base.fail(data=f"创建项目失败: {str(e)}")


@router.get("/{project_id}", response_model=ResponseModel, summary="获取API项目详情")
async def get_project(project_id: int = Path(..., description="项目ID")) -> ResponseModel | ResponseSchemaModel:
    """
    根据ID获取API项目详情
    """
    try:
        project = await ProjectService.get_project_by_id(project_id)
        if not project:
            return response_base.fail(data="项目不存在")

        project_response = ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            base_url=project.base_url,
            headers=project.headers,
            variables=project.variables,
            status=project.status,
            created_time=project.created_time.isoformat() if project.created_time else "",
            updated_time=project.updated_time.isoformat() if project.updated_time else ""
        )
        return response_base.success(data=project_response.model_dump())
    except Exception as e:
        return response_base.fail(data=f"获取项目失败: {str(e)}")


@router.get("", response_model=ResponseModel, summary="获取API项目列表")
async def get_projects(
        skip: int = Query(0, description="跳过数量"),
        limit: int = Query(100, description="限制数量")
) -> ResponseModel | ResponseSchemaModel:
    """
    获取API项目列表
    """
    try:
        projects = await ProjectService.get_projects(skip=skip, limit=limit)
        total = await ProjectService.get_project_count()

        project_list = []
        for project in projects:
            project_response = ProjectResponse(
                id=project.id,
                name=project.name,
                description=project.description,
                base_url=project.base_url,
                headers=project.headers,
                variables=project.variables,
                status=project.status,
                created_time=project.created_time.isoformat() if project.created_time else "",
                updated_time=project.updated_time.isoformat() if project.updated_time else ""
            )
            project_list.append(project_response.model_dump())

        return response_base.success(
            data={
                "items": project_list,
                "total": total,
                "skip": skip,
                "limit": limit
            }
        )
    except Exception as e:
        return response_base.fail(data=f"获取项目列表失败: {str(e)}")


@router.put("/{project_id}", response_model=ResponseModel, summary="更新API项目")
async def update_project(
        project_data: ProjectUpdateRequest,
        project_id: int = Path(..., description="项目ID")
) -> ResponseModel | ResponseSchemaModel:
    """
    更新API项目
    """
    try:
        project = await ProjectService.update_project(project_id, project_data)
        if not project:
            return response_base.fail(data="项目不存在")

        project_response = ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            base_url=project.base_url,
            headers=project.headers,
            variables=project.variables,
            status=project.status,
            created_time=project.created_time.isoformat() if project.created_time else "",
            updated_time=project.updated_time.isoformat() if project.updated_time else ""
        )
        return response_base.success(data=project_response.model_dump())
    except Exception as e:
        return response_base.fail(data=f"更新项目失败: {str(e)}")


@router.delete("/{project_id}", response_model=ResponseModel, summary="删除API项目")
async def delete_project(project_id: int = Path(..., description="项目ID")) -> ResponseModel | ResponseSchemaModel:
    """
    删除API项目
    """
    try:
        success = await ProjectService.delete_project(project_id)
        if not success:
            return response_base.fail(data="项目不存在或删除失败")

        return response_base.success(data="项目删除成功")
    except Exception as e:
        return response_base.fail(data=f"删除项目失败: {str(e)}")
