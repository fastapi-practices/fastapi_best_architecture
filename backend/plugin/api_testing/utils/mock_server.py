#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock服务工具
提供接口Mock功能，类似APIFox的Mock服务
"""
import asyncio
import json
import re
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel, Field, ValidationError
from starlette.middleware.cors import CORSMiddleware
from backend.common.log import log
from backend.database.redis import redis_client
from backend.plugin.api_testing.utils.environment import VariableManager


class MockResponseType(str, Enum):
    """Mock响应类型枚举"""
    JSON = "json"  # JSON数据
    TEXT = "text"  # 文本数据
    XML = "xml"  # XML数据
    HTML = "html"  # HTML数据
    BINARY = "binary"  # 二进制数据


class MockDelayType(str, Enum):
    """Mock延迟类型枚举"""
    NONE = "none"  # 无延迟
    FIXED = "fixed"  # 固定延迟
    RANDOM = "random"  # 随机延迟


class MockScriptType(str, Enum):
    """Mock脚本类型枚举"""
    NONE = "none"  # 无脚本
    PRE_SCRIPT = "pre_script"  # 前置脚本
    POST_SCRIPT = "post_script"  # 后置脚本


class MockDelayConfig(BaseModel):
    """Mock延迟配置"""
    type: MockDelayType = MockDelayType.NONE  # 延迟类型
    fixed_time: Optional[int] = None  # 固定延迟时间(毫秒)
    min_time: Optional[int] = None  # 最小随机延迟时间(毫秒)
    max_time: Optional[int] = None  # 最大随机延迟时间(毫秒)


class MockScriptConfig(BaseModel):
    """Mock脚本配置"""
    type: MockScriptType = MockScriptType.NONE  # 脚本类型
    content: Optional[str] = None  # 脚本内容


class MockHeaderConfig(BaseModel):
    """Mock响应头配置"""
    name: str  # 响应头名称
    value: str  # 响应头值
    enabled: bool = True  # 是否启用


class MockResponse(BaseModel):
    """Mock响应配置"""
    id: str  # 响应ID
    name: str  # 响应名称
    status_code: int = 200  # 状态码
    response_type: MockResponseType = MockResponseType.JSON  # 响应类型
    content: str = "{}"  # 响应内容
    headers: List[MockHeaderConfig] = []  # 响应头
    delay: MockDelayConfig = Field(default_factory=lambda: MockDelayConfig())  # 延迟配置
    script: MockScriptConfig = Field(default_factory=lambda: MockScriptConfig())  # 脚本配置
    weight: int = 1  # 权重，用于随机返回多个响应时的权重计算
    enabled: bool = True  # 是否启用


class MockConditionType(str, Enum):
    """Mock条件类型枚举"""
    PATH = "path"  # 路径匹配
    METHOD = "method"  # 方法匹配
    QUERY = "query"  # 查询参数匹配
    HEADER = "header"  # 请求头匹配
    BODY = "body"  # 请求体匹配
    COOKIE = "cookie"  # Cookie匹配


class MockConditionOperator(str, Enum):
    """Mock条件操作符枚举"""
    EQUALS = "eq"  # 等于
    NOT_EQUALS = "ne"  # 不等于
    CONTAINS = "contains"  # 包含
    NOT_CONTAINS = "not_contains"  # 不包含
    STARTS_WITH = "starts_with"  # 以...开头
    ENDS_WITH = "ends_with"  # 以...结尾
    MATCHES = "matches"  # 正则匹配
    EXISTS = "exists"  # 存在
    NOT_EXISTS = "not_exists"  # 不存在
    GREATER_THAN = "gt"  # 大于
    GREATER_THAN_OR_EQUALS = "gte"  # 大于等于
    LESS_THAN = "lt"  # 小于
    LESS_THAN_OR_EQUALS = "lte"  # 小于等于


class MockCondition(BaseModel):
    """Mock条件配置"""
    id: str  # 条件ID
    type: MockConditionType  # 条件类型
    operator: MockConditionOperator  # 条件操作符
    key: Optional[str] = None  # 条件键，例如请求头名称、查询参数名称等
    value: Optional[Any] = None  # 条件值
    enabled: bool = True  # 是否启用


class MockRule(BaseModel):
    """Mock规则配置"""
    id: str  # 规则ID
    name: str  # 规则名称
    url: str  # 匹配的URL路径
    method: str = "GET"  # HTTP方法
    conditions: List[MockCondition] = []  # 条件列表
    responses: List[MockResponse] = []  # 响应列表
    default_response_id: Optional[str] = None  # 默认响应ID
    enabled: bool = True  # 是否启用
    description: Optional[str] = None  # 规则描述
    project_id: int  # 所属项目ID
    created_at: datetime = Field(default_factory=datetime.now)  # 创建时间
    updated_at: datetime = Field(default_factory=datetime.now)  # 更新时间


class MockProject(BaseModel):
    """Mock项目配置"""
    id: int  # 项目ID
    name: str  # 项目名称
    base_path: str = "/"  # 基础路径
    port: int = 3000  # 端口号
    enabled: bool = True  # 是否启用
    description: Optional[str] = None  # 项目描述
    created_at: datetime = Field(default_factory=datetime.now)  # 创建时间
    updated_at: datetime = Field(default_factory=datetime.now)  # 更新时间


class MockServer:
    """Mock服务"""

    # Redis键前缀
    REDIS_KEY_PREFIX = "api_testing:mock:"

    # 应用实例
    app = FastAPI(title="API Testing Mock Server")

    # 启用CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @classmethod
    async def create_project(cls, project: MockProject) -> bool:
        """
        创建Mock项目
        
        :param project: 项目配置
        :return: 是否成功
        """
        try:
            # 构建Redis键
            key = cls._build_project_key(project.id)

            # 存储项目配置
            await redis_client.set(key, project.model_dump_json())
            return True
        except Exception as e:
            log.error(f"创建Mock项目失败: {e}")
            return False

    @classmethod
    async def get_project(cls, project_id: int) -> Optional[MockProject]:
        """
        获取Mock项目
        
        :param project_id: 项目ID
        :return: 项目配置
        """
        try:
            # 构建Redis键
            key = cls._build_project_key(project_id)

            # 获取项目配置
            data = await redis_client.get(key)
            if not data:
                return None

            # 解析项目配置
            return MockProject.model_validate_json(data)
        except Exception as e:
            log.error(f"获取Mock项目失败: {e}")
            return None

    @classmethod
    async def update_project(cls, project: MockProject) -> bool:
        """
        更新Mock项目
        
        :param project: 项目配置
        :return: 是否成功
        """
        try:
            # 构建Redis键
            key = cls._build_project_key(project.id)

            # 检查项目是否存在
            exists = await redis_client.exists(key)
            if not exists:
                return False

            # 更新项目配置
            await redis_client.set(key, project.model_dump_json())
            return True
        except Exception as e:
            log.error(f"更新Mock项目失败: {e}")
            return False

    @classmethod
    async def delete_project(cls, project_id: int) -> bool:
        """
        删除Mock项目
        
        :param project_id: 项目ID
        :return: 是否成功
        """
        try:
            # 构建Redis键
            key = cls._build_project_key(project_id)

            # 删除项目配置
            await redis_client.delete(key)

            # 删除项目下的所有规则
            rule_pattern = cls._build_rule_key_pattern(project_id)
            rule_keys = await redis_client.keys(rule_pattern)
            if rule_keys:
                await redis_client.delete(*rule_keys)

            return True
        except Exception as e:
            log.error(f"删除Mock项目失败: {e}")
            return False

    @classmethod
    async def list_projects(cls) -> List[MockProject]:
        """
        获取所有Mock项目
        
        :return: 项目配置列表
        """
        try:
            # 构建Redis键模式
            pattern = f"{cls.REDIS_KEY_PREFIX}project:*"

            # 获取所有项目键
            keys = await redis_client.keys(pattern)

            projects = []
            for key in keys:
                data = await redis_client.get(key)
                if data:
                    projects.append(MockProject.model_validate_json(data))

            return projects
        except Exception as e:
            log.error(f"获取Mock项目列表失败: {e}")
            return []

    @classmethod
    async def create_rule(cls, rule: MockRule) -> bool:
        """
        创建Mock规则
        
        :param rule: 规则配置
        :return: 是否成功
        """
        try:
            # 构建Redis键
            key = cls._build_rule_key(rule)

            # 存储规则配置
            await redis_client.set(key, rule.model_dump_json())
            return True
        except Exception as e:
            log.error(f"创建Mock规则失败: {e}")
            return False

    @classmethod
    async def get_rule(cls, rule_id: str, project_id: int) -> Optional[MockRule]:
        """
        获取Mock规则

        :param rule_id: 规则ID
        :param project_id: 项目ID
        :return: 规则配置
        """
        try:
            # 构建Redis键
            key = f"{cls.REDIS_KEY_PREFIX}rule:{project_id}:{rule_id}"
            # 获取规则配置
            data = await redis_client.get(key)
            if not data:
                return None
            # 解析规则配置
            return MockRule.model_validate_json(data)
        except Exception as e:
            log.error(f"获取Mock规则失败: {e}")
            return None

    @classmethod
    async def update_rule(cls, rule: MockRule) -> bool:
        """
        更新Mock规则
        
        :param rule: 规则配置
        :return: 是否成功
        """
        try:
            # 构建Redis键
            key = cls._build_rule_key(rule)

            # 检查规则是否存在
            exists = await redis_client.exists(key)
            if not exists:
                return False

            # 更新规则配置
            rule.updated_at = datetime.now()
            await redis_client.set(key, rule.model_dump_json())
            return True
        except Exception as e:
            log.error(f"更新Mock规则失败: {e}")
            return False

    @classmethod
    async def delete_rule(cls, rule_id: str, project_id: int) -> bool:
        """
        删除Mock规则
        
        :param rule_id: 规则ID
        :param project_id: 项目ID
        :return: 是否成功
        """
        try:
            # 构建Redis键
            key = f"{cls.REDIS_KEY_PREFIX}rule:{project_id}:{rule_id}"

            # 删除规则配置
            await redis_client.delete(key)
            return True
        except Exception as e:
            log.error(f"删除Mock规则失败: {e}")
            return False

    @classmethod
    async def list_rules(cls, project_id: int) -> List[MockRule]:
        """
        获取项目下的所有Mock规则

        :param project_id: 项目ID
        :return: 规则配置列表
        """
        try:
            pattern = cls._build_rule_key_pattern(project_id)
            keys = await redis_client.keys(pattern)
            rules = []

            for key in keys:
                data = await redis_client.get(key)
                if data:
                    try:
                        # 添加数据验证和错误处理
                        rule_data = json.loads(data) if isinstance(data, str) else data

                        # 检查数据格式，修复不符合要求的字段
                        if 'conditions' in rule_data:
                            if isinstance(rule_data['conditions'], list):
                                # 如果conditions包含非对象元素，过滤或转换
                                rule_data['conditions'] = [
                                    cond for cond in rule_data['conditions']
                                    if isinstance(cond, dict)
                                ]

                        if 'responses' in rule_data:
                            if isinstance(rule_data['responses'], list):
                                # 如果responses包含非对象元素，过滤或转换
                                rule_data['responses'] = [
                                    resp for resp in rule_data['responses']
                                    if isinstance(resp, dict)
                                ]

                        rules.append(MockRule.model_validate(rule_data))
                    except ValidationError as ve:
                        log.warning(f"规则数据格式错误，跳过: {key}, 错误: {ve}")
                        continue
                    except Exception as parse_error:
                        log.warning(f"解析规则数据失败，跳过: {key}, 错误: {parse_error}")
                        continue

            return rules
        except Exception as e:
            log.error(f"获取Mock规则列表失败: {e}")
            return []

    @classmethod
    async def process_mock_request(cls, request: Request, project_id: int) -> Optional[Response]:
        """
        处理Mock请求
        
        :param request: FastAPI请求
        :param project_id: 项目ID
        :return: 响应对象，如果没有匹配的规则则返回None
        """
        try:
            # 获取请求路径和方法
            path = request.url.path
            method = request.method

            # 获取项目配置
            project = await cls.get_project(project_id)
            if not project or not project.enabled:
                return None

            # 移除基础路径前缀
            base_path = project.base_path.rstrip('/')
            if path.startswith(base_path):
                path = path[len(base_path):]
                if not path.startswith('/'):
                    path = '/' + path

            # 获取项目下的所有规则
            rules = await cls.list_rules(project_id)
            if not rules:
                return None

            # 过滤出已启用的规则
            rules = [rule for rule in rules if rule.enabled]

            # 查找匹配的规则
            matched_rule = None
            for rule in rules:
                if cls._match_url(rule.url, path) and rule.method.upper() == method.upper():
                    # 检查额外条件
                    if await cls._check_conditions(rule.conditions, request):
                        matched_rule = rule
                        break

            if not matched_rule:
                return None

            # 选择响应
            response_config = await cls._select_response(matched_rule, request)
            if not response_config:
                return None

            # 应用延迟
            await cls._apply_delay(response_config.delay)

            # 执行脚本
            if response_config.script.type != MockScriptType.NONE and response_config.script.content:
                context = {
                    "request": request,
                    "response_content": response_config.content,
                    "variables": {}
                }
                await cls._execute_script(response_config.script.content, context)
                response_config.content = context["response_content"]

            # 处理变量替换
            processed_content = await VariableManager.process_template(response_config.content)

            # 构建响应
            response = await cls._build_response(response_config, processed_content)
            return response
        except Exception as e:
            log.error(f"处理Mock请求失败: {e}")
            return None

    @classmethod
    def register_mock_routes(cls):
        """
        注册Mock路由
        """

        # 动态路由，接收所有请求
        @cls.app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
        async def mock_route(request: Request, path: str):
            # 解析URL中的项目ID参数
            project_id_str = request.query_params.get("_project_id")
            if not project_id_str:
                return Response(
                    content=json.dumps({"error": "Missing _project_id parameter"}),
                    media_type="application/json",
                    status_code=400
                )

            try:
                project_id = int(project_id_str)
            except ValueError:
                return Response(
                    content=json.dumps({"error": "Invalid _project_id parameter"}),
                    media_type="application/json",
                    status_code=400
                )

            # 处理Mock请求
            response = await cls.process_mock_request(request, project_id)
            if not response:
                return Response(
                    content=json.dumps({"error": "No matching mock rule found"}),
                    media_type="application/json",
                    status_code=404
                )

            return response

    @staticmethod
    def _build_project_key(project_id: int) -> str:
        """
        构建项目Redis键
        
        :param project_id: 项目ID
        :return: Redis键
        """
        return f"{MockServer.REDIS_KEY_PREFIX}project:{project_id}"

    @staticmethod
    def _build_rule_key(rule: MockRule) -> str:
        """
        构建规则Redis键
        
        :param rule: 规则配置
        :return: Redis键
        """
        return f"{MockServer.REDIS_KEY_PREFIX}rule:{rule.project_id}:{rule.id}"

    @staticmethod
    def _build_rule_key_pattern(project_id: int) -> str:
        """
        构建规则Redis键模式
        
        :param project_id: 项目ID
        :return: Redis键模式
        """
        return f"{MockServer.REDIS_KEY_PREFIX}rule:{project_id}:*"

    @staticmethod
    def _match_url(rule_url: str, request_url: str) -> bool:
        """
        检查URL是否匹配
        
        :param rule_url: 规则URL
        :param request_url: 请求URL
        :return: 是否匹配
        """
        # 将规则URL转换为正则表达式模式
        pattern = rule_url.replace('/', '\/')

        # 替换路径参数，例如 /users/:id -> /users/([^\/]+)
        pattern = re.sub(r':(\w+)', r'([^\/]+)', pattern)

        # 添加开始和结束标记
        pattern = f'^{pattern}$'

        # 检查是否匹配
        return bool(re.match(pattern, request_url))

    @staticmethod
    async def _check_conditions(conditions: List[MockCondition], request: Request) -> bool:
        """
        检查条件是否匹配
        
        :param conditions: 条件列表
        :param request: FastAPI请求
        :return: 是否匹配
        """
        # 过滤出已启用的条件
        conditions = [condition for condition in conditions if condition.enabled]

        # 如果没有条件，则默认匹配
        if not conditions:
            return True

        # 检查所有条件
        for condition in conditions:
            if not await MockServer._check_single_condition(condition, request):
                return False

        return True

    @staticmethod
    async def _check_single_condition(condition: MockCondition, request: Request) -> bool:
        """
        检查单个条件是否匹配
        
        :param condition: 条件配置
        :param request: FastAPI请求
        :return: 是否匹配
        """
        try:
            if condition.type == MockConditionType.PATH:
                # 路径匹配
                return MockServer._apply_operator(condition.operator, request.url.path, condition.value)
            elif condition.type == MockConditionType.METHOD:
                # 方法匹配
                return MockServer._apply_operator(condition.operator, request.method, condition.value)
            elif condition.type == MockConditionType.QUERY:
                # 查询参数匹配
                query_params = request.query_params
                if condition.operator in [MockConditionOperator.EXISTS, MockConditionOperator.NOT_EXISTS]:
                    return MockServer._apply_operator(condition.operator, condition.key in query_params, None)
                elif condition.key in query_params:
                    return MockServer._apply_operator(condition.operator, query_params[condition.key], condition.value)
                else:
                    return False
            elif condition.type == MockConditionType.HEADER:
                # 请求头匹配
                headers = request.headers
                if condition.operator in [MockConditionOperator.EXISTS, MockConditionOperator.NOT_EXISTS]:
                    return MockServer._apply_operator(condition.operator, condition.key.lower() in headers, None)
                elif condition.key.lower() in headers:
                    return MockServer._apply_operator(
                        condition.operator,
                        headers[condition.key.lower()],
                        condition.value
                    )
                else:
                    return False
            elif condition.type == MockConditionType.BODY:
                # 请求体匹配
                try:
                    # 尝试解析JSON请求体
                    body = await request.json()
                    if '.' in condition.key:
                        # 支持点表示法访问嵌套属性
                        keys = condition.key.split('.')
                        value = body
                        for key in keys:
                            if isinstance(value, dict) and key in value:
                                value = value[key]
                            else:
                                return False
                        return MockServer._apply_operator(condition.operator, value, condition.value)
                    elif condition.operator in [MockConditionOperator.EXISTS, MockConditionOperator.NOT_EXISTS]:
                        return MockServer._apply_operator(condition.operator, condition.key in body, None)
                    elif condition.key in body:
                        return MockServer._apply_operator(condition.operator, body[condition.key], condition.value)
                    else:
                        return False
                except:
                    # 如果不是JSON请求体，尝试获取表单数据
                    try:
                        form = await request.form()
                        if condition.operator in [MockConditionOperator.EXISTS, MockConditionOperator.NOT_EXISTS]:
                            return MockServer._apply_operator(condition.operator, condition.key in form, None)
                        elif condition.key in form:
                            return MockServer._apply_operator(condition.operator, form[condition.key], condition.value)
                        else:
                            return False
                    except:
                        # 如果获取表单数据也失败，则无法匹配
                        return False
            elif condition.type == MockConditionType.COOKIE:
                # Cookie匹配
                cookies = request.cookies
                if condition.operator in [MockConditionOperator.EXISTS, MockConditionOperator.NOT_EXISTS]:
                    return MockServer._apply_operator(condition.operator, condition.key in cookies, None)
                elif condition.key in cookies:
                    return MockServer._apply_operator(condition.operator, cookies[condition.key], condition.value)
                else:
                    return False
            else:
                return False
        except Exception as e:
            log.error(f"检查条件失败: {e}")
            return False

    @staticmethod
    def _apply_operator(operator: MockConditionOperator, actual_value: Any, expected_value: Any) -> bool:
        """
        应用条件操作符
        
        :param operator: 条件操作符
        :param actual_value: 实际值
        :param expected_value: 期望值
        :return: 是否匹配
        """
        if operator == MockConditionOperator.EQUALS:
            return actual_value == expected_value
        elif operator == MockConditionOperator.NOT_EQUALS:
            return actual_value != expected_value
        elif operator == MockConditionOperator.CONTAINS:
            if isinstance(actual_value, str) and isinstance(expected_value, str):
                return expected_value in actual_value
            elif isinstance(actual_value, (list, tuple, dict)):
                return expected_value in actual_value
            else:
                return False
        elif operator == MockConditionOperator.NOT_CONTAINS:
            if isinstance(actual_value, str) and isinstance(expected_value, str):
                return expected_value not in actual_value
            elif isinstance(actual_value, (list, tuple, dict)):
                return expected_value not in actual_value
            else:
                return True
        elif operator == MockConditionOperator.STARTS_WITH:
            return isinstance(actual_value, str) and isinstance(expected_value, str) and actual_value.startswith(
                expected_value
            )
        elif operator == MockConditionOperator.ENDS_WITH:
            return isinstance(actual_value, str) and isinstance(expected_value, str) and actual_value.endswith(
                expected_value
            )
        elif operator == MockConditionOperator.MATCHES:
            return isinstance(actual_value, str) and isinstance(expected_value, str) and bool(
                re.match(expected_value, actual_value)
            )
        elif operator == MockConditionOperator.EXISTS:
            return bool(actual_value)
        elif operator == MockConditionOperator.NOT_EXISTS:
            return not bool(actual_value)
        elif operator == MockConditionOperator.GREATER_THAN:
            try:
                return float(actual_value) > float(expected_value)
            except:
                return False
        elif operator == MockConditionOperator.GREATER_THAN_OR_EQUALS:
            try:
                return float(actual_value) >= float(expected_value)
            except:
                return False
        elif operator == MockConditionOperator.LESS_THAN:
            try:
                return float(actual_value) < float(expected_value)
            except:
                return False
        elif operator == MockConditionOperator.LESS_THAN_OR_EQUALS:
            try:
                return float(actual_value) <= float(expected_value)
            except:
                return False
        else:
            return False

    @staticmethod
    async def _select_response(rule: MockRule, request: Request) -> Optional[MockResponse]:
        """
        选择响应
        
        :param rule: 规则配置
        :param request: FastAPI请求
        :return: 响应配置
        """
        # 过滤出已启用的响应
        responses = [response for response in rule.responses if response.enabled]
        if not responses:
            return None

        # 如果只有一个响应，则直接返回
        if len(responses) == 1:
            return responses[0]

        # 如果有默认响应，且默认响应已启用，则返回默认响应
        if rule.default_response_id:
            for response in responses:
                if response.id == rule.default_response_id:
                    return response

        # 如果有多个响应，则根据权重随机选择
        total_weight = sum(response.weight for response in responses)
        if total_weight <= 0:
            # 如果总权重小于等于0，则均匀随机选择
            import random
            return random.choice(responses)

        # 根据权重随机选择
        import random
        r = random.uniform(0, total_weight)
        cumulative_weight = 0
        for response in responses:
            cumulative_weight += response.weight
            if r <= cumulative_weight:
                return response

        # 如果随机选择失败，则返回第一个响应
        return responses[0]

    @staticmethod
    async def _apply_delay(delay_config: MockDelayConfig) -> None:
        """
        应用延迟
        
        :param delay_config: 延迟配置
        """
        if delay_config.type == MockDelayType.NONE:
            return

        if delay_config.type == MockDelayType.FIXED and delay_config.fixed_time:
            await asyncio.sleep(delay_config.fixed_time / 1000)
        elif delay_config.type == MockDelayType.RANDOM and delay_config.min_time and delay_config.max_time:
            import random
            delay = random.uniform(delay_config.min_time, delay_config.max_time)
            await asyncio.sleep(delay / 1000)

    @staticmethod
    async def _execute_script(script: str, context: Dict[str, Any]) -> None:
        """
        执行Mock脚本
        
        :param script: 脚本内容
        :param context: 脚本上下文
        """
        try:
            # 为了安全，限制脚本的执行环境
            safe_globals = {
                "json": json,
                "re": re,
                "time": time,
                "datetime": datetime,
                "context": context,
                "log": log
            }

            # 执行脚本
            exec(script, safe_globals)
        except Exception as e:
            log.error(f"执行Mock脚本失败: {e}")

    @staticmethod
    async def _build_response(response_config: MockResponse, content: str) -> Response:
        """
        构建响应
        
        :param response_config: 响应配置
        :param content: 响应内容
        :return: FastAPI响应
        """
        # 设置内容类型
        content_type = "application/json"
        if response_config.response_type == MockResponseType.TEXT:
            content_type = "text/plain"
        elif response_config.response_type == MockResponseType.XML:
            content_type = "application/xml"
        elif response_config.response_type == MockResponseType.HTML:
            content_type = "text/html"
        elif response_config.response_type == MockResponseType.BINARY:
            content_type = "application/octet-stream"

        # 构建响应头
        headers = {}
        for header in response_config.headers:
            if header.enabled:
                headers[header.name] = header.value

        # 构建响应
        response = Response(
            content=content,
            status_code=response_config.status_code,
            media_type=content_type,
            headers=headers
        )

        return response


# 注册Mock路由
MockServer.register_mock_routes()
