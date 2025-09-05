#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试用例管理接口
"""
from typing import List, Optional
from fastapi import APIRouter, Path, Query, HTTPException
from backend.common.response.response_schema import response_base, ResponseModel, ResponseSchemaModel
from backend.plugin.api_testing.service.test_case_service import TestCaseService
from backend.plugin.api_testing.schema.request import (
    TestCaseCreateRequest, TestCaseUpdateRequest, TestCaseResponse
)

router = APIRouter()


@router.post("/", response_model=ResponseModel, summary="创建测试用例")
async def create_test_case(case_data: TestCaseCreateRequest) -> ResponseModel | ResponseSchemaModel:
    """
    创建测试用例
    """
    try:
        test_case = await TestCaseService.create_test_case(case_data)
        case_response = TestCaseResponse(
            id=test_case.id,
            name=test_case.name,
            project_id=test_case.project_id,
            description=test_case.description,
            pre_script=test_case.pre_script,
            post_script=test_case.post_script,
            status=test_case.status,
            created_time=test_case.created_time.isoformat() if test_case.created_time else "",
            updated_time=test_case.updated_time.isoformat() if test_case.updated_time else ""
        )
        return response_base.success(data=case_response.model_dump())
    except Exception as e:
        return response_base.fail(data=f"创建测试用例失败: {str(e)}")


@router.get("/{case_id}", response_model=ResponseModel, summary="获取测试用例详情")
async def get_test_case(case_id: int = Path(..., description="用例ID")) -> ResponseModel | ResponseSchemaModel:
    """
    根据ID获取测试用例详情
    """
    try:
        test_case = await TestCaseService.get_test_case_by_id(case_id)
        if not test_case:
            return response_base.fail(data="测试用例不存在")
        
        case_response = TestCaseResponse(
            id=test_case.id,
            name=test_case.name,
            project_id=test_case.project_id,
            description=test_case.description,
            pre_script=test_case.pre_script,
            post_script=test_case.post_script,
            status=test_case.status,
            created_time=test_case.created_time.isoformat() if test_case.created_time else "",
            updated_time=test_case.updated_time.isoformat() if test_case.updated_time else ""
        )
        return response_base.success(data=case_response.model_dump())
    except Exception as e:
        return response_base.fail(data=f"获取测试用例失败: {str(e)}")


@router.get("/", response_model=ResponseModel, summary="获取测试用例列表")
async def get_test_cases(
    project_id: Optional[int] = Query(None, description="项目ID"),
    skip: int = Query(0, description="跳过数量"),
    limit: int = Query(100, description="限制数量")
) -> ResponseModel | ResponseSchemaModel:
    """
    获取测试用例列表
    """
    try:
        test_cases = await TestCaseService.get_test_cases(project_id=project_id, skip=skip, limit=limit)
        total = await TestCaseService.get_test_case_count(project_id=project_id)
        
        case_list = []
        for test_case in test_cases:
            case_response = TestCaseResponse(
                id=test_case.id,
                name=test_case.name,
                project_id=test_case.project_id,
                description=test_case.description,
                pre_script=test_case.pre_script,
                post_script=test_case.post_script,
                status=test_case.status,
                created_time=test_case.created_time.isoformat() if test_case.created_time else "",
                updated_time=test_case.updated_time.isoformat() if test_case.updated_time else ""
            )
            case_list.append(case_response.model_dump())
        
        return response_base.success(data={
            "items": case_list,
            "total": total,
            "skip": skip,
            "limit": limit,
            "project_id": project_id
        })
    except Exception as e:
        return response_base.fail(data=f"获取测试用例列表失败: {str(e)}")


@router.put("/{case_id}", response_model=ResponseModel, summary="更新测试用例")
async def update_test_case(
    case_data: TestCaseUpdateRequest,
    case_id: int = Path(..., description="用例ID")
) -> ResponseModel | ResponseSchemaModel:
    """
    更新测试用例
    """
    try:
        test_case = await TestCaseService.update_test_case(case_id, case_data)
        if not test_case:
            return response_base.fail(data="测试用例不存在")
        
        case_response = TestCaseResponse(
            id=test_case.id,
            name=test_case.name,
            project_id=test_case.project_id,
            description=test_case.description,
            pre_script=test_case.pre_script,
            post_script=test_case.post_script,
            status=test_case.status,
            created_time=test_case.created_time.isoformat() if test_case.created_time else "",
            updated_time=test_case.updated_time.isoformat() if test_case.updated_time else ""
        )
        return response_base.success(data=case_response.model_dump())
    except Exception as e:
        return response_base.fail(data=f"更新测试用例失败: {str(e)}")


@router.delete("/{case_id}", response_model=ResponseModel, summary="删除测试用例")
async def delete_test_case(case_id: int = Path(..., description="用例ID")) -> ResponseModel | ResponseSchemaModel:
    """
    删除测试用例
    """
    try:
        success = await TestCaseService.delete_test_case(case_id)
        if not success:
            return response_base.fail(data="测试用例不存在或删除失败")
        
        return response_base.success(data="测试用例删除成功")
    except Exception as e:
        return response_base.fail(data=f"删除测试用例失败: {str(e)}")
