#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL执行API
"""
from typing import Any, Dict, List

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from backend.common.response.response_schema import response_base
from backend.plugin.api_testing.utils.sql_executor import SQLExecutor, SQLQuery

router = APIRouter()


@router.post("/execute", response_model=Dict[str, Any], summary="执行SQL查询")
async def execute_sql_query(query: SQLQuery) -> JSONResponse:
    """
    执行SQL查询接口
    
    执行指定的SQL查询并返回结果
    """
    try:
        # 执行SQL查询
        result = await SQLExecutor.execute_query(query)
        
        return response_base.success(data=result.model_dump())
    except Exception as e:
        return response_base.fail(msg=f"SQL执行失败: {str(e)}")


@router.post("/batch-execute", response_model=Dict[str, Any], summary="批量执行SQL查询")
async def execute_batch_sql_queries(queries: List[SQLQuery]) -> JSONResponse:
    """
    批量执行SQL查询接口
    
    批量执行指定的SQL查询并返回结果列表
    """
    try:
        results = []
        for query in queries:
            result = await SQLExecutor.execute_query(query)
            results.append(result.model_dump())
        
        # 构建响应
        data = {
            "results": results,
            "summary": {
                "total": len(results),
                "success": sum(1 for result in results if result["success"]),
                "failed": sum(1 for result in results if not result["success"])
            }
        }
        
        return response_base.success(data=data)
    except Exception as e:
        return response_base.fail(msg=f"批量SQL执行失败: {str(e)}")