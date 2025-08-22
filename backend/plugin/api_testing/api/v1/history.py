#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
接口历史记录API
提供接口请求历史记录的API
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from backend.common.response.response_schema import response_base
from backend.plugin.api_testing.utils.history import HistoryManager, RequestHistoryItem

router = APIRouter()


class HistoryFilter(BaseModel):
    """历史记录过滤条件"""
    project_id: Optional[str] = Field(default=None, description="项目ID")
    start_time: Optional[datetime] = Field(default=None, description="开始时间")
    end_time: Optional[datetime] = Field(default=None, description="结束时间")
    url_contains: Optional[str] = Field(default=None, description="URL包含字符串")
    method: Optional[str] = Field(default=None, description="HTTP方法")
    tags: Optional[List[str]] = Field(default=None, description="标签列表")
    successful: Optional[bool] = Field(default=None, description="是否成功")


@router.post("", response_model=Dict[str, Any], summary="添加历史记录")
async def add_history(history: RequestHistoryItem = Body(...)) -> JSONResponse:
    """
    添加接口请求历史记录
    
    添加一条接口请求历史记录并返回其ID
    """
    try:
        history_id = await HistoryManager.add_history(history)
        return response_base.success(data={"id": history_id})
    except Exception as e:
        return response_base.fail(msg=f"添加历史记录失败: {str(e)}")


@router.get("/{history_id}", response_model=Dict[str, Any], summary="获取历史记录详情")
async def get_history(
    history_id: str,
    project_id: Optional[str] = None
) -> JSONResponse:
    """
    获取历史记录详情
    
    根据历史记录ID获取详细信息
    """
    try:
        history = await HistoryManager.get_history(history_id, project_id)
        if history:
            return response_base.success(data=history.model_dump())
        else:
            return response_base.fail(msg=f"历史记录 {history_id} 不存在")
    except Exception as e:
        return response_base.fail(msg=f"获取历史记录失败: {str(e)}")


@router.get("", response_model=Dict[str, Any], summary="获取历史记录列表")
async def get_history_list(
    project_id: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000, description="每页记录数"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    url_contains: Optional[str] = None,
    method: Optional[str] = None,
    successful: Optional[bool] = None
) -> JSONResponse:
    """
    获取历史记录列表
    
    根据条件获取历史记录列表，支持分页和过滤
    """
    try:
        histories = await HistoryManager.get_history_list(
            project_id=project_id,
            limit=limit,
            skip=skip,
            start_time=start_time,
            end_time=end_time,
            url_contains=url_contains,
            method=method,
            successful=successful
        )
        
        # 计算总记录数
        total_count = len(await HistoryManager.get_history_list(
            project_id=project_id,
            limit=0,  # 不限制数量
            start_time=start_time,
            end_time=end_time,
            url_contains=url_contains,
            method=method,
            successful=successful
        ))
        
        # 构建响应数据
        data = {
            "items": [h.model_dump() for h in histories],
            "pagination": {
                "total": total_count,
                "limit": limit,
                "skip": skip,
                "page": skip // limit + 1 if limit > 0 else 1,
                "pages": (total_count + limit - 1) // limit if limit > 0 else 1
            }
        }
        
        return response_base.success(data=data)
    except Exception as e:
        return response_base.fail(msg=f"获取历史记录列表失败: {str(e)}")


@router.post("/filter", response_model=Dict[str, Any], summary="按条件过滤历史记录")
async def filter_history(
    filter_params: HistoryFilter = Body(...),
    limit: int = Query(100, ge=1, le=1000, description="每页记录数"),
    skip: int = Query(0, ge=0, description="跳过记录数")
) -> JSONResponse:
    """
    按条件过滤历史记录
    
    使用更复杂的条件过滤历史记录列表
    """
    try:
        histories = await HistoryManager.get_history_list(
            project_id=filter_params.project_id,
            limit=limit,
            skip=skip,
            start_time=filter_params.start_time,
            end_time=filter_params.end_time,
            url_contains=filter_params.url_contains,
            method=filter_params.method,
            tags=filter_params.tags,
            successful=filter_params.successful
        )
        
        # 计算总记录数
        total_count = len(await HistoryManager.get_history_list(
            project_id=filter_params.project_id,
            limit=0,  # 不限制数量
            start_time=filter_params.start_time,
            end_time=filter_params.end_time,
            url_contains=filter_params.url_contains,
            method=filter_params.method,
            tags=filter_params.tags,
            successful=filter_params.successful
        ))
        
        # 构建响应数据
        data = {
            "items": [h.model_dump() for h in histories],
            "pagination": {
                "total": total_count,
                "limit": limit,
                "skip": skip,
                "page": skip // limit + 1 if limit > 0 else 1,
                "pages": (total_count + limit - 1) // limit if limit > 0 else 1
            },
            "filter": filter_params.model_dump()
        }
        
        return response_base.success(data=data)
    except Exception as e:
        return response_base.fail(msg=f"过滤历史记录失败: {str(e)}")


@router.delete("/{history_id}", response_model=Dict[str, Any], summary="删除历史记录")
async def delete_history(
    history_id: str,
    project_id: Optional[str] = None
) -> JSONResponse:
    """
    删除历史记录
    
    根据历史记录ID删除记录
    """
    try:
        deleted = await HistoryManager.delete_history(history_id, project_id)
        if deleted:
            return response_base.success(data={"deleted": True, "id": history_id})
        else:
            return response_base.fail(msg=f"历史记录 {history_id} 不存在或删除失败")
    except Exception as e:
        return response_base.fail(msg=f"删除历史记录失败: {str(e)}")


@router.delete("", response_model=Dict[str, Any], summary="清空历史记录")
async def clear_history(
    project_id: Optional[str] = None
) -> JSONResponse:
    """
    清空历史记录
    
    清空指定项目或所有项目的历史记录
    """
    try:
        count = await HistoryManager.clear_history(project_id)
        project_info = f"项目 {project_id}" if project_id else "所有项目"
        return response_base.success(data={"cleared": True, "count": count, "project_id": project_id}, msg=f"已清空{project_info}的{count}条历史记录")
    except Exception as e:
        return response_base.fail(msg=f"清空历史记录失败: {str(e)}")


@router.get("/statistics", response_model=Dict[str, Any], summary="获取历史记录统计信息")
async def get_history_stats(
    project_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> JSONResponse:
    """
    获取历史记录统计信息
    
    获取历史记录的统计信息，包括总数、成功率等
    """
    try:
        # 获取所有符合条件的历史记录
        histories = await HistoryManager.get_history_list(
            project_id=project_id,
            limit=0,  # 不限制数量
            start_time=start_time,
            end_time=end_time
        )
        
        total_count = len(histories)
        if total_count == 0:
            # 没有记录时返回空统计
            stats = {
                "total_count": 0,
                "success_count": 0,
                "failure_count": 0,
                "success_rate": 0,
                "avg_response_time": 0,
                "methods": {},
                "status_codes": {}
            }
        else:
            # 计算统计数据
            success_count = sum(1 for h in histories if h.is_successful())
            failure_count = total_count - success_count
            success_rate = success_count / total_count if total_count > 0 else 0
            
            # 计算平均响应时间
            response_times = [h.response_time for h in histories if h.response_time is not None]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            # 按HTTP方法分组
            methods = {}
            for h in histories:
                method = h.method.upper()
                methods[method] = methods.get(method, 0) + 1
            
            # 按状态码分组
            status_codes = {}
            for h in histories:
                if h.status_code is not None:
                    status_code = str(h.status_code)
                    status_codes[status_code] = status_codes.get(status_code, 0) + 1
            
            stats = {
                "total_count": total_count,
                "success_count": success_count,
                "failure_count": failure_count,
                "success_rate": success_rate,
                "avg_response_time": avg_response_time,
                "methods": methods,
                "status_codes": status_codes
            }
        
        return response_base.success(data=stats)
    except Exception as e:
        return response_base.fail(msg=f"获取历史记录统计信息失败: {str(e)}")