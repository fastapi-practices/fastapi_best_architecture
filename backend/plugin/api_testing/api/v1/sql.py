#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL执行API
"""
from typing import Any, Dict, List
from fastapi import APIRouter
from backend.common.response.response_schema import response_base, ResponseModel, ResponseSchemaModel
from backend.plugin.api_testing.utils.sql_executor import SQLExecutor, SQLQuery

router = APIRouter()


@router.post("/execute", response_model=Dict[str, Any], summary="执行SQL查询")
async def execute_sql_query(query: SQLQuery) -> ResponseModel:
    """
    执行SQL查询接口
    
    执行指定的SQL查询并返回结果
    """
    try:
        # 执行SQL查询
        result = await SQLExecutor.execute_query(query)
        response = response_base.success(data=result.model_dump())
        return response.model_dump()
    except Exception as e:
        response = response_base.fail(data=f"SQL执行失败: {str(e)}")
        return response.model_dump()


@router.post("/batch-execute", response_model=Dict[str, Any], summary="批量执行SQL查询")
async def execute_batch_sql_queries(queries: List[SQLQuery]) -> Dict[str, Any]:
    """
    批量执行SQL查询接口

    批量执行指定的SQL查询并返回结果列表
    """
    try:
        results = []
        for query in queries:
            try:
                result = await SQLExecutor.execute_query(query)
                response = response_base.success(data=result.model_dump())
                results.append(response.model_dump())
            except Exception as query_error:
                # 单个查询失败时，记录错误但继续执行其他查询
                error_response = response_base.fail(data=f"查询执行失败: {str(query_error)}")
                results.append(error_response.model_dump())
        # 构建响应
        data = {
            "results": results,
            "summary": {
                "total": len(results),
                "success": sum(1 for result in results if result.get("success", False)),
                "failed": sum(1 for result in results if not result.get("success", True))
            }
        }

        return {
            "code": 200,
            "msg": "批量执行完成",
            "data": data,
            "success": True
        }
    except Exception as e:
        return {
            "code": 400,
            "msg": "请求错误",
            "data": f"批量SQL执行失败: {str(e)}",
            "success": False
        }
