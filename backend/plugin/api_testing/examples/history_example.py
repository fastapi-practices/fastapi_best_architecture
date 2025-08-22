#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
接口历史记录使用示例
演示如何记录、查询和分析接口请求历史
"""
import json
import time
from datetime import datetime, timedelta

import requests

BASE_URL = "http://localhost:8000/v1/api_testing"


def send_request_and_record_history():
    """发送请求并记录历史"""
    # 1. 发送API请求
    request_start = time.time()
    response = requests.post(
        f"{BASE_URL}/requests/send",
        json={
            "url": "https://jsonplaceholder.typicode.com/posts/1",
            "method": "GET",
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        }
    )
    request_end = time.time()
    response_time = (request_end - request_start) * 1000  # 转换为毫秒
    response_data = response.json()

    # 2. 记录历史
    history_response = requests.post(
        f"{BASE_URL}/history",
        json={
            "name": "获取博客文章",
            "url": "https://jsonplaceholder.typicode.com/posts/1",
            "method": "GET",
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            "status_code": response.status_code,
            "response_headers": dict(response.headers),
            "response_body": response_data.get("data", {}).get("response", {}),
            "response_time": response_time,
            "project_id": "demo_project",
            "tags": ["demo", "api_test"]
        }
    )
    
    history_data = history_response.json()
    history_id = history_data.get("data", {}).get("id")
    
    print(f"请求已记录，历史记录ID: {history_id}")
    return history_id


def query_history(history_id):
    """查询历史记录详情"""
    response = requests.get(
        f"{BASE_URL}/history/{history_id}",
        params={"project_id": "demo_project"}
    )
    
    if response.status_code == 200:
        history_data = response.json().get("data", {})
        print("历史记录详情:")
        print(f"请求名称: {history_data.get('name')}")
        print(f"请求URL: {history_data.get('url')}")
        print(f"请求方法: {history_data.get('method')}")
        print(f"响应状态码: {history_data.get('status_code')}")
        print(f"响应时间: {history_data.get('response_time'):.2f} ms")
    else:
        print(f"查询历史记录失败: {response.text}")


def query_history_list():
    """查询历史记录列表"""
    response = requests.get(
        f"{BASE_URL}/history",
        params={
            "project_id": "demo_project",
            "limit": 10,
            "skip": 0
        }
    )
    
    if response.status_code == 200:
        history_list = response.json().get("data", {}).get("items", [])
        pagination = response.json().get("data", {}).get("pagination", {})
        
        print(f"历史记录总数: {pagination.get('total')}")
        print("最近的历史记录:")
        
        for i, history in enumerate(history_list):
            print(f"{i+1}. {history.get('name')} - {history.get('url')} ({history.get('method')}) - "
                  f"状态码: {history.get('status_code')}, 时间: {history.get('timestamp')}")
    else:
        print(f"查询历史记录列表失败: {response.text}")


def filter_history_by_conditions():
    """按条件过滤历史记录"""
    # 计算一周前的时间
    one_week_ago = datetime.now() - timedelta(days=7)
    
    response = requests.post(
        f"{BASE_URL}/history/filter",
        params={"limit": 10, "skip": 0},
        json={
            "project_id": "demo_project",
            "start_time": one_week_ago.isoformat(),
            "method": "GET",
            "url_contains": "jsonplaceholder",
            "successful": True
        }
    )
    
    if response.status_code == 200:
        history_list = response.json().get("data", {}).get("items", [])
        filter_info = response.json().get("data", {}).get("filter", {})
        
        print(f"过滤条件: {json.dumps(filter_info, indent=2)}")
        print(f"找到 {len(history_list)} 条符合条件的记录")
        
        for i, history in enumerate(history_list):
            print(f"{i+1}. {history.get('name')} - {history.get('url')}")
    else:
        print(f"过滤历史记录失败: {response.text}")


def get_history_statistics():
    """获取历史记录统计信息"""
    response = requests.get(
        f"{BASE_URL}/history/statistics",
        params={"project_id": "demo_project"}
    )
    
    if response.status_code == 200:
        stats = response.json().get("data", {})
        
        print("历史记录统计信息:")
        print(f"总请求数: {stats.get('total_count')}")
        print(f"成功请求: {stats.get('success_count')}")
        print(f"失败请求: {stats.get('failure_count')}")
        print(f"成功率: {stats.get('success_rate') * 100:.2f}%")
        print(f"平均响应时间: {stats.get('avg_response_time'):.2f} ms")
        
        print("按HTTP方法分布:")
        for method, count in stats.get("methods", {}).items():
            print(f"  {method}: {count}次")
        
        print("按状态码分布:")
        for status, count in stats.get("status_codes", {}).items():
            print(f"  {status}: {count}次")
    else:
        print(f"获取统计信息失败: {response.text}")


def clear_project_history():
    """清空项目历史记录"""
    response = requests.delete(
        f"{BASE_URL}/history",
        params={"project_id": "demo_project"}
    )
    
    if response.status_code == 200:
        result = response.json().get("data", {})
        print(f"已清空历史记录: {result.get('count')}条")
    else:
        print(f"清空历史记录失败: {response.text}")


if __name__ == "__main__":
    # 演示完整流程
    print("===== 接口历史记录功能演示 =====")
    
    # 1. 发送请求并记录历史
    print("\n1. 发送请求并记录历史:")
    history_id = send_request_and_record_history()
    
    # 2. 查询历史记录详情
    print("\n2. 查询历史记录详情:")
    query_history(history_id)
    
    # 3. 查询历史记录列表
    print("\n3. 查询历史记录列表:")
    query_history_list()
    
    # 4. 按条件过滤历史记录
    print("\n4. 按条件过滤历史记录:")
    filter_history_by_conditions()
    
    # 5. 获取历史记录统计信息
    print("\n5. 获取历史记录统计信息:")
    get_history_statistics()
    
    # 注释掉以下代码，避免清空所有历史记录
    # print("\n6. 清空项目历史记录:")
    # clear_project_history()