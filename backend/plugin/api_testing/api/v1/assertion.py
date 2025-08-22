#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
断言API
"""
from typing import Any, Dict, List

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from backend.common.response.response_schema import response_base
from backend.plugin.api_testing.utils.assertion import Assertion, AssertionEngine, AssertionResult

router = APIRouter()


@router.post("/validate", response_model=Dict[str, Any], summary="执行断言验证")
async def execute_assertion(
    assertion: Assertion = Body(...),
    response_data: Dict[str, Any] = Body(...)
) -> JSONResponse:
    """
    执行断言验证接口
    
    根据提供的断言配置和响应数据执行断言验证，返回断言结果
    """
    try:
        # 执行断言
        result = AssertionEngine.execute_assertion(assertion, response_data)
        
        return response_base.success(data=result.model_dump())
    except Exception as e:
        return response_base.fail(msg=f"断言执行失败: {str(e)}")


@router.post("/batch-validate", response_model=Dict[str, Any], summary="批量执行断言验证")
async def execute_batch_assertions(
    assertions: List[Assertion] = Body(...),
    response_data: Dict[str, Any] = Body(...)
) -> JSONResponse:
    """
    批量执行断言验证接口
    
    根据提供的断言配置列表和响应数据执行批量断言验证，返回断言结果列表
    """
    try:
        # 执行批量断言
        results = AssertionEngine.execute_assertions(assertions, response_data)
        
        # 构建响应
        data = {
            "results": [result.model_dump() for result in results],
            "summary": {
                "total": len(results),
                "success": sum(1 for result in results if result.success),
                "failed": sum(1 for result in results if not result.success)
            }
        }
        
        return response_base.success(data=data)
    except Exception as e:
        return response_base.fail(msg=f"批量断言执行失败: {str(e)}")