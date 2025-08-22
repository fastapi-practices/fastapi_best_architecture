#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
失败分析工具
提供对API接口失败原因的详细分析
"""
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class FailureType(str, Enum):
    """失败类型枚举"""
    CONNECTION_ERROR = "connection_error"  # 连接错误
    TIMEOUT = "timeout"  # 超时
    SSL_ERROR = "ssl_error"  # SSL证书错误
    STATUS_CODE_ERROR = "status_code_error"  # 状态码错误
    ASSERTION_ERROR = "assertion_error"  # 断言失败
    SQL_ERROR = "sql_error"  # SQL执行错误
    DATA_EXTRACT_ERROR = "data_extract_error"  # 数据提取错误
    UNEXPECTED_RESPONSE = "unexpected_response"  # 意外响应
    SERVER_ERROR = "server_error"  # 服务器错误
    CLIENT_ERROR = "client_error"  # 客户端错误
    UNKNOWN = "unknown"  # 未知错误


class FailureDetail(BaseModel):
    """失败详情模型"""
    type: FailureType  # 失败类型
    message: str  # 失败消息
    suggestion: Optional[str] = None  # 解决建议
    related_data: Optional[Dict[str, Any]] = None  # 相关数据


class FailureAnalysisResult(BaseModel):
    """失败分析结果"""
    primary_cause: FailureDetail  # 主要原因
    secondary_causes: Optional[List[FailureDetail]] = None  # 次要原因
    diff_data: Optional[Dict[str, Any]] = None  # 期望值与实际值的差异
    code_snippets: Optional[Dict[str, str]] = None  # 相关代码片段


class FailureAnalyzer:
    """失败分析器"""
    
    @staticmethod
    def analyze_response_failure(response_data: Dict[str, Any]) -> Optional[FailureDetail]:
        """
        分析HTTP响应失败
        
        :param response_data: 响应数据
        :return: 失败详情
        """
        if not response_data:
            return FailureDetail(
                type=FailureType.UNKNOWN,
                message="没有响应数据"
            )
            
        # 检查是否有错误信息
        if response_data.get("error"):
            error_msg = response_data["error"]
            
            # 连接错误
            if "connection" in error_msg.lower():
                return FailureDetail(
                    type=FailureType.CONNECTION_ERROR,
                    message=f"连接错误: {error_msg}",
                    suggestion="检查网络连接和服务器状态，确保目标服务可访问"
                )
                
            # 超时错误
            elif "timeout" in error_msg.lower():
                return FailureDetail(
                    type=FailureType.TIMEOUT,
                    message=f"请求超时: {error_msg}",
                    suggestion="增加超时时间或检查服务器性能问题"
                )
                
            # SSL错误
            elif "ssl" in error_msg.lower() or "certificate" in error_msg.lower():
                return FailureDetail(
                    type=FailureType.SSL_ERROR,
                    message=f"SSL证书错误: {error_msg}",
                    suggestion="检查SSL证书配置或设置verify_ssl=False（不推荐用于生产环境）"
                )
            
            # 未知错误
            else:
                return FailureDetail(
                    type=FailureType.UNKNOWN,
                    message=f"未知错误: {error_msg}"
                )
                
        # 检查状态码
        status_code = response_data.get("status_code", 0)
        
        # 客户端错误 (4xx)
        if 400 <= status_code < 500:
            error_type = FailureType.CLIENT_ERROR
            message = f"客户端错误，状态码: {status_code}"
            suggestion = "检查请求参数、认证信息和请求格式"
            
            # 特定状态码的具体建议
            if status_code == 400:
                suggestion = "请求格式错误，检查请求参数和格式"
            elif status_code == 401:
                suggestion = "未授权，检查认证信息是否正确"
            elif status_code == 403:
                suggestion = "禁止访问，检查用户权限"
            elif status_code == 404:
                suggestion = "资源不存在，检查URL是否正确"
            elif status_code == 429:
                suggestion = "请求过多，遵循API限制或降低请求频率"
            
            return FailureDetail(
                type=error_type,
                message=message,
                suggestion=suggestion,
                related_data={"status_code": status_code}
            )
            
        # 服务器错误 (5xx)
        elif 500 <= status_code < 600:
            return FailureDetail(
                type=FailureType.SERVER_ERROR,
                message=f"服务器错误，状态码: {status_code}",
                suggestion="检查服务器日志，可能是服务器内部错误",
                related_data={"status_code": status_code}
            )
            
        return None
    
    @staticmethod
    def analyze_assertion_failure(assertion_results: List[Dict[str, Any]]) -> List[FailureDetail]:
        """
        分析断言失败
        
        :param assertion_results: 断言结果列表
        :return: 失败详情列表
        """
        failures = []
        
        for result in assertion_results:
            if not result.get("success", True):
                assertion = result.get("assertion", {})
                
                failure = FailureDetail(
                    type=FailureType.ASSERTION_ERROR,
                    message=f"断言失败: {result.get('message', '未知原因')}",
                    related_data={
                        "assertion_type": assertion.get("type"),
                        "expected": assertion.get("expected"),
                        "actual": result.get("actual"),
                        "path": assertion.get("path")
                    }
                )
                
                # 根据断言类型添加建议
                assertion_type = assertion.get("type", "")
                if "equals" in assertion_type:
                    failure.suggestion = "检查期望值和实际值是否一致，注意数据类型"
                elif "contains" in assertion_type:
                    failure.suggestion = "检查实际值是否包含期望的子字符串或元素"
                elif "match" in assertion_type:
                    failure.suggestion = "检查正则表达式是否正确匹配实际值"
                elif "length" in assertion_type:
                    failure.suggestion = "检查数组、字符串或集合的长度是否符合预期"
                elif "exists" in assertion_type:
                    failure.suggestion = "检查期望的字段或值是否存在"
                else:
                    failure.suggestion = "检查断言条件是否合理"
                
                failures.append(failure)
        
        return failures
    
    @staticmethod
    def analyze_sql_failure(sql_results: List[Dict[str, Any]]) -> List[FailureDetail]:
        """
        分析SQL执行失败
        
        :param sql_results: SQL执行结果列表
        :return: 失败详情列表
        """
        failures = []
        
        for result in sql_results:
            if not result.get("success", True):
                error = result.get("error", "未知SQL错误")
                query = result.get("query", "")
                
                message = f"SQL执行失败: {error}"
                suggestion = "检查SQL语法和数据库连接"
                
                # 根据错误信息分类
                if "syntax" in error.lower():
                    suggestion = "SQL语法错误，检查查询语句"
                elif "permission" in error.lower() or "access denied" in error.lower():
                    suggestion = "数据库权限不足，检查用户权限"
                elif "connection" in error.lower():
                    suggestion = "数据库连接错误，检查连接参数和网络"
                elif "timeout" in error.lower():
                    suggestion = "查询超时，考虑优化SQL或增加超时时间"
                elif "does not exist" in error.lower() or "not found" in error.lower():
                    if "table" in error.lower():
                        suggestion = "表不存在，检查表名"
                    elif "column" in error.lower():
                        suggestion = "列不存在，检查列名"
                    else:
                        suggestion = "对象不存在，检查名称"
                
                failure = FailureDetail(
                    type=FailureType.SQL_ERROR,
                    message=message,
                    suggestion=suggestion,
                    related_data={
                        "query": query,
                        "error": error
                    }
                )
                
                failures.append(failure)
        
        return failures
    
    @staticmethod
    def analyze_step_failure(step_data: Dict[str, Any]) -> FailureAnalysisResult:
        """
        分析测试步骤失败
        
        :param step_data: 步骤数据
        :return: 失败分析结果
        """
        primary_cause = None
        secondary_causes = []
        
        # 检查响应错误
        response = step_data.get("response", {})
        response_failure = FailureAnalyzer.analyze_response_failure(response)
        if response_failure:
            primary_cause = response_failure
        
        # 检查断言失败
        assertion_results = step_data.get("assertions", [])
        assertion_failures = FailureAnalyzer.analyze_assertion_failure(assertion_results)
        if assertion_failures:
            if not primary_cause:
                primary_cause = assertion_failures[0]
                secondary_causes.extend(assertion_failures[1:]) if len(assertion_failures) > 1 else None
            else:
                secondary_causes.extend(assertion_failures)
        
        # 检查SQL执行失败
        sql_results = step_data.get("sql_results", [])
        sql_failures = FailureAnalyzer.analyze_sql_failure(sql_results)
        if sql_failures:
            if not primary_cause:
                primary_cause = sql_failures[0]
                secondary_causes.extend(sql_failures[1:]) if len(sql_failures) > 1 else None
            else:
                secondary_causes.extend(sql_failures)
        
        # 如果没有找到具体失败原因
        if not primary_cause:
            primary_cause = FailureDetail(
                type=FailureType.UNKNOWN,
                message="未能确定具体失败原因",
                suggestion="检查请求参数和期望结果"
            )
        
        # 构建差异数据
        diff_data = {}
        for assertion in assertion_failures:
            if assertion.related_data:
                key = f"assertion_{assertion.related_data.get('assertion_type', 'unknown')}"
                diff_data[key] = {
                    "expected": assertion.related_data.get("expected"),
                    "actual": assertion.related_data.get("actual"),
                    "path": assertion.related_data.get("path")
                }
        
        return FailureAnalysisResult(
            primary_cause=primary_cause,
            secondary_causes=secondary_causes if secondary_causes else None,
            diff_data=diff_data if diff_data else None,
            code_snippets=None  # 可以在未来版本中添加相关代码片段
        )