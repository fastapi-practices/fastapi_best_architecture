#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
断言工具模块
提供接口响应断言功能
"""
import json
import re
from enum import Enum
from typing import Any, Dict, List, Union, Optional

from jsonpath_ng import parse
from pydantic import BaseModel


class AssertionType(str, Enum):
    """断言类型枚举"""
    EQUALS = "equals"  # 等于
    NOT_EQUALS = "not_equals"  # 不等于
    CONTAINS = "contains"  # 包含
    NOT_CONTAINS = "not_contains"  # 不包含
    STARTS_WITH = "starts_with"  # 以...开头
    ENDS_WITH = "ends_with"  # 以...结尾
    MATCH_REGEX = "match_regex"  # 匹配正则表达式
    LESS_THAN = "less_than"  # 小于
    LESS_THAN_OR_EQUALS = "less_than_or_equals"  # 小于或等于
    GREATER_THAN = "greater_than"  # 大于
    GREATER_THAN_OR_EQUALS = "greater_than_or_equals"  # 大于或等于
    EXISTS = "exists"  # 存在
    NOT_EXISTS = "not_exists"  # 不存在
    IS_EMPTY = "is_empty"  # 为空
    IS_NOT_EMPTY = "is_not_empty"  # 不为空
    IS_NULL = "is_null"  # 为null
    IS_NOT_NULL = "is_not_null"  # 不为null
    IS_TRUE = "is_true"  # 为true
    IS_FALSE = "is_false"  # 为false
    LENGTH_EQUALS = "length_equals"  # 长度等于
    LENGTH_GREATER_THAN = "length_greater_than"  # 长度大于
    LENGTH_LESS_THAN = "length_less_than"  # 长度小于


class AssertionSource(str, Enum):
    """断言来源枚举"""
    STATUS_CODE = "status_code"  # HTTP状态码
    HEADERS = "headers"  # 响应头
    COOKIES = "cookies"  # Cookies
    BODY = "body"  # 响应体
    JSON = "json"  # JSON响应体


class Assertion(BaseModel):
    """断言配置模型"""
    source: AssertionSource  # 断言来源
    type: AssertionType  # 断言类型
    path: Optional[str] = None  # 值路径，例如JSONPath表达式 $.data.id
    expected: Optional[Any] = None  # 预期值
    message: Optional[str] = None  # 断言消息


class AssertionResult(BaseModel):
    """断言结果模型"""
    assertion: Assertion  # 原始断言配置
    success: bool  # 断言结果
    actual: Optional[Any] = None  # 实际值
    message: Optional[str] = None  # 结果消息


class AssertionEngine:
    """断言引擎"""

    @staticmethod
    def get_value_by_path(data: Any, path: str) -> Any:
        """
        通过路径获取数据值
        
        :param data: 数据源
        :param path: 路径表达式
        :return: 提取的值
        """
        if not path:
            return data
            
        # 对于字典类型，使用JSONPath提取
        if isinstance(data, (dict, list)):
            try:
                jsonpath_expr = parse(path)
                matches = [match.value for match in jsonpath_expr.find(data)]
                if not matches:
                    return None
                return matches[0] if len(matches) == 1 else matches
            except Exception:
                return None
                
        return None
        
    @staticmethod
    def execute_assertion(assertion: Assertion, response_data: Dict[str, Any]) -> AssertionResult:
        """
        执行断言
        
        :param assertion: 断言配置
        :param response_data: 响应数据，格式如 {"status_code": 200, "headers": {...}, "body": "...", "json": {...}}
        :return: 断言结果
        """
        source_data = None
        
        # 获取断言来源数据
        if assertion.source == AssertionSource.STATUS_CODE:
            source_data = response_data.get("status_code")
        elif assertion.source == AssertionSource.HEADERS:
            source_data = response_data.get("headers", {})
        elif assertion.source == AssertionSource.COOKIES:
            source_data = response_data.get("cookies", {})
        elif assertion.source == AssertionSource.BODY:
            source_data = response_data.get("body", "")
        elif assertion.source == AssertionSource.JSON:
            source_data = response_data.get("json")
        
        # 如果来源数据不存在
        if source_data is None and assertion.type not in (AssertionType.IS_NULL, AssertionType.NOT_EXISTS):
            return AssertionResult(
                assertion=assertion,
                success=False,
                actual=None,
                message=f"断言来源 {assertion.source} 不存在"
            )
        
        # 如果有path，先获取对应的值
        actual_value = None
        if assertion.path and assertion.source not in (AssertionSource.STATUS_CODE, AssertionSource.BODY):
            actual_value = AssertionEngine.get_value_by_path(source_data, assertion.path)
        else:
            actual_value = source_data
        
        # 执行断言
        success = False
        message = None
        
        try:
            # 根据断言类型执行对应的断言逻辑
            if assertion.type == AssertionType.EQUALS:
                success = actual_value == assertion.expected
                message = f"期望值: {assertion.expected}, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.NOT_EQUALS:
                success = actual_value != assertion.expected
                message = f"期望值不等于: {assertion.expected}, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.CONTAINS:
                if isinstance(actual_value, (str, list, dict)):
                    success = assertion.expected in actual_value
                message = f"期望包含: {assertion.expected}, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.NOT_CONTAINS:
                if isinstance(actual_value, (str, list, dict)):
                    success = assertion.expected not in actual_value
                message = f"期望不包含: {assertion.expected}, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.STARTS_WITH:
                if isinstance(actual_value, str):
                    success = actual_value.startswith(assertion.expected)
                message = f"期望以 {assertion.expected} 开头, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.ENDS_WITH:
                if isinstance(actual_value, str):
                    success = actual_value.endswith(assertion.expected)
                message = f"期望以 {assertion.expected} 结尾, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.MATCH_REGEX:
                if isinstance(actual_value, str):
                    success = bool(re.match(assertion.expected, actual_value))
                message = f"期望匹配正则: {assertion.expected}, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.LESS_THAN:
                if isinstance(actual_value, (int, float)) and isinstance(assertion.expected, (int, float)):
                    success = actual_value < assertion.expected
                message = f"期望小于: {assertion.expected}, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.LESS_THAN_OR_EQUALS:
                if isinstance(actual_value, (int, float)) and isinstance(assertion.expected, (int, float)):
                    success = actual_value <= assertion.expected
                message = f"期望小于等于: {assertion.expected}, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.GREATER_THAN:
                if isinstance(actual_value, (int, float)) and isinstance(assertion.expected, (int, float)):
                    success = actual_value > assertion.expected
                message = f"期望大于: {assertion.expected}, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.GREATER_THAN_OR_EQUALS:
                if isinstance(actual_value, (int, float)) and isinstance(assertion.expected, (int, float)):
                    success = actual_value >= assertion.expected
                message = f"期望大于等于: {assertion.expected}, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.EXISTS:
                success = actual_value is not None
                message = f"期望存在, 实际: {'存在' if success else '不存在'}"
                
            elif assertion.type == AssertionType.NOT_EXISTS:
                success = actual_value is None
                message = f"期望不存在, 实际: {'不存在' if success else '存在'}"
                
            elif assertion.type == AssertionType.IS_EMPTY:
                success = not actual_value
                message = f"期望为空, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.IS_NOT_EMPTY:
                success = bool(actual_value)
                message = f"期望不为空, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.IS_NULL:
                success = actual_value is None
                message = f"期望为null, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.IS_NOT_NULL:
                success = actual_value is not None
                message = f"期望不为null, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.IS_TRUE:
                success = actual_value is True
                message = f"期望为true, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.IS_FALSE:
                success = actual_value is False
                message = f"期望为false, 实际值: {actual_value}"
                
            elif assertion.type == AssertionType.LENGTH_EQUALS:
                if hasattr(actual_value, "__len__"):
                    success = len(actual_value) == assertion.expected
                message = f"期望长度等于: {assertion.expected}, 实际长度: {len(actual_value) if hasattr(actual_value, '__len__') else 'N/A'}"
                
            elif assertion.type == AssertionType.LENGTH_GREATER_THAN:
                if hasattr(actual_value, "__len__"):
                    success = len(actual_value) > assertion.expected
                message = f"期望长度大于: {assertion.expected}, 实际长度: {len(actual_value) if hasattr(actual_value, '__len__') else 'N/A'}"
                
            elif assertion.type == AssertionType.LENGTH_LESS_THAN:
                if hasattr(actual_value, "__len__"):
                    success = len(actual_value) < assertion.expected
                message = f"期望长度小于: {assertion.expected}, 实际长度: {len(actual_value) if hasattr(actual_value, '__len__') else 'N/A'}"
            
            else:
                message = f"不支持的断言类型: {assertion.type}"
        
        except Exception as e:
            message = f"断言执行异常: {str(e)}"
            success = False
        
        # 自定义消息
        if assertion.message:
            message = f"{assertion.message}: {message}"
        
        return AssertionResult(
            assertion=assertion,
            success=success,
            actual=actual_value,
            message=message
        )
    
    @staticmethod
    def execute_assertions(assertions: List[Assertion], response_data: Dict[str, Any]) -> List[AssertionResult]:
        """
        批量执行断言
        
        :param assertions: 断言配置列表
        :param response_data: 响应数据
        :return: 断言结果列表
        """
        results = []
        for assertion in assertions:
            result = AssertionEngine.execute_assertion(assertion, response_data)
            results.append(result)
        return results