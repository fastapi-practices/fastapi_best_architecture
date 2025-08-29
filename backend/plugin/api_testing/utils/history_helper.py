#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史记录辅助工具
提供快速记录和分析接口历史的辅助函数
"""
import httpx
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from backend.plugin.api_testing.utils.history import HistoryManager, RequestHistoryItem


class HistoryHelper:
    """历史记录辅助工具类"""
    
    @staticmethod
    async def record_request(
        request_info: Dict[str, Any],
        response_info: Dict[str, Any],
        project_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        记录请求历史
        
        :param request_info: 请求信息
        :param response_info: 响应信息
        :param project_id: 项目ID
        :param tags: 标签列表
        :param metadata: 其他元数据
        :return: 历史记录ID
        """
        # 构建历史记录项
        history_item = RequestHistoryItem(
            name=request_info.get("name", f"{request_info.get('method', 'GET')} {request_info.get('url', '')}"),
            url=request_info.get("url", ""),
            method=request_info.get("method", "GET"),
            headers=request_info.get("headers", {}),
            params=request_info.get("params", {}),
            body=request_info.get("body"),
            status_code=response_info.get("status_code"),
            response_headers=response_info.get("headers", {}),
            response_body=response_info.get("body"),
            response_time=response_info.get("response_time"),
            project_id=project_id,
            tags=tags or [],
            error=response_info.get("error")
        )
        
        # 添加其他元数据
        if metadata:
            for key, value in metadata.items():
                if hasattr(history_item, key):
                    setattr(history_item, key, value)
        
        # 记录历史
        history_id = await HistoryManager.add_history(history_item)
        return history_id
    
    @staticmethod
    async def track_request(
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        project_id: Optional[str] = None,
        name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """
        发送并记录HTTP请求
        
        :param url: 请求URL
        :param method: 请求方法
        :param headers: 请求头
        :param params: 查询参数
        :param data: 请求数据
        :param json: JSON请求数据
        :param project_id: 项目ID
        :param name: 请求名称
        :param tags: 标签列表
        :param timeout: 超时时间（秒）
        :return: 包含响应和历史记录ID的字典
        """
        # 准备请求信息
        request_info = {
            "name": name or f"{method} {url}",
            "url": url,
            "method": method,
            "headers": headers or {},
            "params": params or {},
            "body": data or json
        }
        
        # 发送请求并计时
        start_time = time.time()
        error = None
        response = None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    data=data,
                    json=json,
                    timeout=timeout
                )
                
            # 计算响应时间（毫秒）
            response_time = (time.time() - start_time) * 1000
            
            # 获取响应信息
            response_info = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": response.text,  # 先保存为文本
                "response_time": response_time
            }
            
            # 尝试解析JSON响应
            try:
                response_info["body"] = response.json()
            except Exception:
                pass  # 如果不是JSON，保留文本格式
                
        except Exception as e:
            # 处理请求异常
            error = str(e)
            response_time = (time.time() - start_time) * 1000
            response_info = {
                "status_code": None,
                "headers": {},
                "body": None,
                "response_time": response_time,
                "error": error
            }
        
        # 记录历史
        history_id = await HistoryHelper.record_request(
            request_info=request_info,
            response_info=response_info,
            project_id=project_id,
            tags=tags
        )
        
        # 返回结果
        result = {
            "request": request_info,
            "response": response_info,
            "history_id": history_id
        }
        
        if error:
            result["error"] = error
        
        if response:
            result["status_code"] = response.status_code
            result["is_success"] = 200 <= response.status_code < 400
        
        return result
    
    @staticmethod
    async def get_recent_stats(
        project_id: Optional[str] = None,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        获取最近一段时间的请求统计信息
        
        :param project_id: 项目ID
        :param days: 天数
        :return: 统计信息
        """
        # 计算时间范围
        end_time = datetime.now()
        start_time = end_time.replace(hour=0, minute=0, second=0, microsecond=0) - \
                    datetime.timedelta(days=days)
        
        # 获取历史记录
        histories = await HistoryManager.get_history_list(
            project_id=project_id,
            limit=0,  # 不限制数量
            start_time=start_time,
            end_time=end_time
        )
        
        # 按日期分组统计
        daily_stats = {}
        for history in histories:
            # 获取日期
            date_key = history.timestamp.strftime("%Y-%m-%d")
            
            # 初始化日期统计
            if date_key not in daily_stats:
                daily_stats[date_key] = {
                    "total": 0,
                    "success": 0,
                    "failure": 0,
                    "avg_time": 0,
                    "total_time": 0
                }
            
            # 更新统计
            stats = daily_stats[date_key]
            stats["total"] += 1
            
            if history.is_successful():
                stats["success"] += 1
            else:
                stats["failure"] += 1
                
            if history.response_time:
                stats["total_time"] += history.response_time
                stats["avg_time"] = stats["total_time"] / stats["total"]
        
        # 汇总统计
        total_requests = sum(stats["total"] for stats in daily_stats.values())
        total_success = sum(stats["success"] for stats in daily_stats.values())
        total_failure = sum(stats["failure"] for stats in daily_stats.values())
        all_response_times = [h.response_time for h in histories if h.response_time]
        avg_response_time = sum(all_response_times) / len(all_response_times) if all_response_times else 0
        
        # 返回结果
        return {
            "summary": {
                "total_requests": total_requests,
                "success_requests": total_success,
                "failure_requests": total_failure,
                "success_rate": total_success / total_requests if total_requests > 0 else 0,
                "avg_response_time": avg_response_time
            },
            "daily": daily_stats,
            "period": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "days": days
            }
        }