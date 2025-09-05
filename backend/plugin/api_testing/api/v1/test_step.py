#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试步骤管理接口
"""
from typing import List, Optional
from fastapi import APIRouter, Path, Query, HTTPException
from backend.common.response.response_schema import response_base, ResponseModel, ResponseSchemaModel
from backend.plugin.api_testing.service.test_step_service import TestStepService
from backend.plugin.api_testing.schema.request import (
    TestStepCreateRequest, TestStepUpdateRequest, TestStepResponse, StepReorderRequest
)

router = APIRouter()


@router.post("/", response_model=ResponseModel, summary="创建测试步骤")
async def create_test_step(step_data: TestStepCreateRequest) -> ResponseModel | ResponseSchemaModel:
    """
    创建测试步骤
    """
    try:
        test_step = await TestStepService.create_test_step(step_data)
        step_response = TestStepResponse(
            id=test_step.id,
            name=test_step.name,
            test_case_id=test_step.test_case_id,
            url=test_step.url,
            method=test_step.method,
            headers=test_step.headers,
            params=test_step.params,
            body=test_step.body,
            files=test_step.files,
            auth=test_step.auth,
            extract=test_step.extract,
            validations=test_step.validate,
            sql_queries=test_step.sql_queries,
            timeout=test_step.timeout,
            retry=test_step.retry,
            retry_interval=test_step.retry_interval,
            order=test_step.order,
            status=test_step.status,
            created_time=test_step.created_time.isoformat() if test_step.created_time else "",
            updated_time=test_step.updated_time.isoformat() if test_step.updated_time else ""
        )
        return response_base.success(data=step_response.model_dump())
    except ValueError as e:
        # 处理业务逻辑错误（如测试用例不存在、参数超出范围）
        return response_base.fail(data=str(e))
    except Exception as e:
        # 处理其他未预期的错误
        return response_base.fail(data=f"创建测试步骤失败: {str(e)}")


@router.get("/{step_id}", response_model=ResponseModel, summary="获取测试步骤详情")
async def get_test_step(step_id: int = Path(..., description="步骤ID")) -> ResponseModel | ResponseSchemaModel:
    """
    根据ID获取测试步骤详情
    """
    try:
        test_step = await TestStepService.get_test_step_by_id(step_id)
        if not test_step:
            return response_base.fail(data="测试步骤不存在")
        
        step_response = TestStepResponse(
            id=test_step.id,
            name=test_step.name,
            test_case_id=test_step.test_case_id,
            url=test_step.url,
            method=test_step.method,
            headers=test_step.headers,
            params=test_step.params,
            body=test_step.body,
            files=test_step.files,
            auth=test_step.auth,
            extract=test_step.extract,
            validations=test_step.validate,
            sql_queries=test_step.sql_queries,
            timeout=test_step.timeout,
            retry=test_step.retry,
            retry_interval=test_step.retry_interval,
            order=test_step.order,
            status=test_step.status,
            created_time=test_step.created_time.isoformat() if test_step.created_time else "",
            updated_time=test_step.updated_time.isoformat() if test_step.updated_time else ""
        )
        return response_base.success(data=step_response.model_dump())
    except Exception as e:
        return response_base.fail(data=f"获取测试步骤失败: {str(e)}")


@router.get("/", response_model=ResponseModel, summary="获取测试步骤列表")
async def get_test_steps(
    test_case_id: Optional[int] = Query(None, description="测试用例ID"),
    skip: int = Query(0, description="跳过数量"),
    limit: int = Query(100, description="限制数量")
) -> ResponseModel | ResponseSchemaModel:
    """
    获取测试步骤列表
    """
    try:
        test_steps = await TestStepService.get_test_steps(test_case_id=test_case_id, skip=skip, limit=limit)
        total = await TestStepService.get_test_step_count(test_case_id=test_case_id)
        
        step_list = []
        for test_step in test_steps:
            step_response = TestStepResponse(
                id=test_step.id,
                name=test_step.name,
                test_case_id=test_step.test_case_id,
                url=test_step.url,
                method=test_step.method,
                headers=test_step.headers,
                params=test_step.params,
                body=test_step.body,
                files=test_step.files,
                auth=test_step.auth,
                extract=test_step.extract,
                validations=test_step.validate,
                sql_queries=test_step.sql_queries,
                timeout=test_step.timeout,
                retry=test_step.retry,
                retry_interval=test_step.retry_interval,
                order=test_step.order,
                status=test_step.status,
                created_time=test_step.created_time.isoformat() if test_step.created_time else "",
                updated_time=test_step.updated_time.isoformat() if test_step.updated_time else ""
            )
            step_list.append(step_response.model_dump())
        
        return response_base.success(data={
            "items": step_list,
            "total": total,
            "skip": skip,
            "limit": limit,
            "test_case_id": test_case_id
        })
    except Exception as e:
        return response_base.fail(data=f"获取测试步骤列表失败: {str(e)}")


@router.put("/{step_id}", response_model=ResponseModel, summary="更新测试步骤")
async def update_test_step(
    step_data: TestStepUpdateRequest,
    step_id: int = Path(..., description="步骤ID")
) -> ResponseModel | ResponseSchemaModel:
    """
    更新测试步骤
    """
    try:
        test_step = await TestStepService.update_test_step(step_id, step_data)
        if not test_step:
            return response_base.fail(data="测试步骤不存在")
        
        step_response = TestStepResponse(
            id=test_step.id,
            name=test_step.name,
            test_case_id=test_step.test_case_id,
            url=test_step.url,
            method=test_step.method,
            headers=test_step.headers,
            params=test_step.params,
            body=test_step.body,
            files=test_step.files,
            auth=test_step.auth,
            extract=test_step.extract,
            validations=test_step.validate,
            sql_queries=test_step.sql_queries,
            timeout=test_step.timeout,
            retry=test_step.retry,
            retry_interval=test_step.retry_interval,
            order=test_step.order,
            status=test_step.status,
            created_time=test_step.created_time.isoformat() if test_step.created_time else "",
            updated_time=test_step.updated_time.isoformat() if test_step.updated_time else ""
        )
        return response_base.success(data=step_response.model_dump())
    except Exception as e:
        return response_base.fail(data=f"更新测试步骤失败: {str(e)}")


@router.delete("/{step_id}", response_model=ResponseModel, summary="删除测试步骤")
async def delete_test_step(step_id: int = Path(..., description="步骤ID")) -> ResponseModel | ResponseSchemaModel:
    """
    删除测试步骤
    """
    try:
        success = await TestStepService.delete_test_step(step_id)
        if not success:
            return response_base.fail(data="测试步骤不存在或删除失败")
        
        return response_base.success(data="测试步骤删除成功")
    except Exception as e:
        return response_base.fail(data=f"删除测试步骤失败: {str(e)}")


@router.post("/reorder", response_model=ResponseModel, summary="重新排序测试步骤")
async def reorder_test_steps(
    reorder_data: StepReorderRequest,
    test_case_id: int = Query(..., description="测试用例ID")
) -> ResponseModel | ResponseSchemaModel:
    """
    重新排序测试步骤
    """
    try:
        success = await TestStepService.reorder_steps(test_case_id, reorder_data.step_orders)
        if not success:
            return response_base.fail(data="步骤排序失败")
        
        return response_base.success(data="步骤排序成功")
    except Exception as e:
        return response_base.fail(data=f"步骤排序失败: {str(e)}")
