#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境变量管理工具
提供类似APIFox的环境变量管理功能
"""
import json
import os
import re
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union, Tuple

from pydantic import BaseModel, Field

from backend.common.log import log
from backend.core.path_conf import PLUGIN_DIR
from backend.database.redis import redis_client


class VariableScope(str, Enum):
    """变量作用域枚举"""
    GLOBAL = "global"  # 全局变量，所有项目共享
    PROJECT = "project"  # 项目变量，项目内共享
    ENVIRONMENT = "environment"  # 环境变量，特定环境共享
    CASE = "case"  # 用例变量，仅当前用例可用
    TEMPORARY = "temporary"  # 临时变量，仅当前请求可用


class EnvironmentType(str, Enum):
    """环境类型枚举"""
    DEVELOPMENT = "development"  # 开发环境
    TESTING = "testing"  # 测试环境
    STAGING = "staging"  # 预发布环境
    PRODUCTION = "production"  # 生产环境
    CUSTOM = "custom"  # 自定义环境


class VariableModel(BaseModel):
    """变量模型"""
    name: str  # 变量名
    value: Any  # 变量值
    description: Optional[str] = None  # 变量描述
    scope: VariableScope  # 变量作用域
    environment_id: Optional[int] = None  # 环境ID，仅当scope=ENVIRONMENT时需要
    project_id: Optional[int] = None  # 项目ID，仅当scope=PROJECT时需要
    case_id: Optional[int] = None  # 用例ID，仅当scope=CASE时需要
    is_encrypted: bool = False  # 是否加密存储


class EnvironmentModel(BaseModel):
    """环境模型"""
    id: int  # 环境ID
    name: str  # 环境名称
    type: EnvironmentType  # 环境类型
    base_url: str  # 基础URL
    description: Optional[str] = None  # 环境描述
    project_id: int  # 所属项目ID
    is_default: bool = False  # 是否为默认环境


class VariableManager:
    """变量管理器"""

    # Redis键前缀
    REDIS_KEY_PREFIX = "api_testing:variable:"

    @classmethod
    async def set_variable(cls, variable: VariableModel) -> bool:
        """
        设置变量
        
        :param variable: 变量信息
        :return: 是否成功
        """
        try:
            # 构建Redis键
            key = cls._build_variable_key(variable)

            # 加密敏感数据
            if variable.is_encrypted:
                variable.value = cls._encrypt_value(variable.value)

            # 存储变量
            await redis_client.set(key, variable.model_dump_json())
            return True
        except Exception as e:
            log.error(f"设置变量失败: {e}")
            return False

    @classmethod
    async def get_variable(
            cls,
            name: str,
            scope: VariableScope,
            project_id: Optional[int] = None,
            environment_id: Optional[int] = None,
            case_id: Optional[int] = None
    ) -> Optional[VariableModel]:
        """
        获取变量
        
        :param name: 变量名
        :param scope: 变量作用域
        :param project_id: 项目ID
        :param environment_id: 环境ID
        :param case_id: 用例ID
        :return: 变量信息
        """
        try:
            # 构建Redis键
            key = cls._build_variable_key_by_params(
                name=name,
                scope=scope,
                project_id=project_id,
                environment_id=environment_id,
                case_id=case_id
            )

            # 获取变量
            data = await redis_client.get(key)
            if not data:
                return None

            # 解析变量
            variable = VariableModel.model_validate_json(data)

            # 解密敏感数据
            if variable.is_encrypted:
                variable.value = cls._decrypt_value(variable.value)

            return variable
        except Exception as e:
            log.error(f"获取变量失败: {e}")
            return None

    @classmethod
    async def delete_variable(
            cls,
            name: str,
            scope: VariableScope,
            project_id: Optional[int] = None,
            environment_id: Optional[int] = None,
            case_id: Optional[int] = None
    ) -> bool:
        """
        删除变量
        
        :param name: 变量名
        :param scope: 变量作用域
        :param project_id: 项目ID
        :param environment_id: 环境ID
        :param case_id: 用例ID
        :return: 是否成功
        """
        try:
            # 构建Redis键
            key = cls._build_variable_key_by_params(
                name=name,
                scope=scope,
                project_id=project_id,
                environment_id=environment_id,
                case_id=case_id
            )

            # 删除变量
            await redis_client.delete(key)
            return True
        except Exception as e:
            log.error(f"删除变量失败: {e}")
            return False

    @classmethod
    async def list_variables(
            cls,
            scope: VariableScope,
            project_id: Optional[int] = None,
            environment_id: Optional[int] = None,
            case_id: Optional[int] = None
    ) -> List[VariableModel]:
        """
        获取变量列表
        
        :param scope: 变量作用域
        :param project_id: 项目ID
        :param environment_id: 环境ID
        :param case_id: 用例ID
        :return: 变量列表
        """
        try:
            # 构建Redis键模式
            pattern = cls._build_variable_key_pattern(scope, project_id, environment_id, case_id)

            # 获取所有匹配的键
            keys = await redis_client.keys(pattern)

            variables = []
            for key in keys:
                data = await redis_client.get(key)
                if data:
                    variable = VariableModel.model_validate_json(data)

                    # 解密敏感数据
                    if variable.is_encrypted:
                        variable.value = cls._decrypt_value(variable.value)

                    variables.append(variable)

            return variables
        except Exception as e:
            log.error(f"获取变量列表失败: {e}")
            return []

    @classmethod
    async def process_template(
            cls,
            template: str,
            project_id: Optional[int] = None,
            environment_id: Optional[int] = None,
            case_id: Optional[int] = None,
            temp_variables: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        处理变量模板
        替换形如 {{variable_name}} 的变量引用
        
        :param template: 模板字符串
        :param project_id: 项目ID
        :param environment_id: 环境ID
        :param case_id: 用例ID
        :param temp_variables: 临时变量字典
        :return: 替换后的字符串
        """
        if not template:
            return template

        # 临时变量字典
        temp_vars = temp_variables or {}

        # 查找所有变量引用
        pattern = r'\{\{(.*?)\}\}'
        matches = re.findall(pattern, template)

        # 如果没有变量引用，直接返回原始模板
        if not matches:
            return template

        # 处理每个变量引用
        result = template
        for match in matches:
            var_name = match.strip()
            value = await cls._get_variable_value(
                var_name,
                project_id,
                environment_id,
                case_id,
                temp_vars
            )

            if value is not None:
                # 替换变量引用
                result = result.replace(f"{{{{{var_name}}}}}", str(value))

        return result

    @classmethod
    async def process_template_dict(
            cls,
            template_dict: Dict[str, Any],
            project_id: Optional[int] = None,
            environment_id: Optional[int] = None,
            case_id: Optional[int] = None,
            temp_variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        处理变量模板字典
        递归替换字典中所有字符串值中的变量引用
        
        :param template_dict: 模板字典
        :param project_id: 项目ID
        :param environment_id: 环境ID
        :param case_id: 用例ID
        :param temp_variables: 临时变量字典
        :return: 替换后的字典
        """
        if not template_dict:
            return template_dict

        result = {}
        for key, value in template_dict.items():
            if isinstance(value, str):
                # 处理字符串值
                result[key] = await cls.process_template(
                    value,
                    project_id,
                    environment_id,
                    case_id,
                    temp_variables
                )
            elif isinstance(value, dict):
                # 递归处理嵌套字典
                result[key] = await cls.process_template_dict(
                    value,
                    project_id,
                    environment_id,
                    case_id,
                    temp_variables
                )
            elif isinstance(value, list):
                # 递归处理列表
                result[key] = await cls.process_template_list(
                    value,
                    project_id,
                    environment_id,
                    case_id,
                    temp_variables
                )
            else:
                # 其他类型值直接复制
                result[key] = value

        return result

    @classmethod
    async def process_template_list(
            cls,
            template_list: List[Any],
            project_id: Optional[int] = None,
            environment_id: Optional[int] = None,
            case_id: Optional[int] = None,
            temp_variables: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """
        处理变量模板列表
        递归替换列表中所有字符串值中的变量引用
        
        :param template_list: 模板列表
        :param project_id: 项目ID
        :param environment_id: 环境ID
        :param case_id: 用例ID
        :param temp_variables: 临时变量字典
        :return: 替换后的列表
        """
        if not template_list:
            return template_list

        result = []
        for item in template_list:
            if isinstance(item, str):
                # 处理字符串值
                result.append(
                    await cls.process_template(
                        item,
                        project_id,
                        environment_id,
                        case_id,
                        temp_variables
                    )
                )
            elif isinstance(item, dict):
                # 递归处理嵌套字典
                result.append(
                    await cls.process_template_dict(
                        item,
                        project_id,
                        environment_id,
                        case_id,
                        temp_variables
                    )
                )
            elif isinstance(item, list):
                # 递归处理嵌套列表
                result.append(
                    await cls.process_template_list(
                        item,
                        project_id,
                        environment_id,
                        case_id,
                        temp_variables
                    )
                )
            else:
                # 其他类型值直接复制
                result.append(item)

        return result

    @classmethod
    async def _get_variable_value(
            cls,
            name: str,
            project_id: Optional[int] = None,
            environment_id: Optional[int] = None,
            case_id: Optional[int] = None,
            temp_variables: Dict[str, Any] = None
    ) -> Any:
        """
        按优先级获取变量值
        优先级: 临时变量 > 用例变量 > 环境变量 > 项目变量 > 全局变量
        
        :param name: 变量名
        :param project_id: 项目ID
        :param environment_id: 环境ID
        :param case_id: 用例ID
        :param temp_variables: 临时变量字典
        :return: 变量值，未找到则为None
        """
        # 检查临时变量
        if temp_variables and name in temp_variables:
            return temp_variables[name]

        # 检查用例变量
        if case_id:
            case_var = await cls.get_variable(name, VariableScope.CASE, case_id=case_id)
            if case_var:
                return case_var.value

        # 检查环境变量
        if environment_id:
            env_var = await cls.get_variable(name, VariableScope.ENVIRONMENT, environment_id=environment_id)
            if env_var:
                return env_var.value

        # 检查项目变量
        if project_id:
            proj_var = await cls.get_variable(name, VariableScope.PROJECT, project_id=project_id)
            if proj_var:
                return proj_var.value

        # 检查全局变量
        global_var = await cls.get_variable(name, VariableScope.GLOBAL)
        if global_var:
            return global_var.value

        # 未找到变量
        return None

    @staticmethod
    def _build_variable_key(variable: VariableModel) -> str:
        """
        构建变量Redis键
        
        :param variable: 变量信息
        :return: Redis键
        """
        prefix = VariableManager.REDIS_KEY_PREFIX

        if variable.scope == VariableScope.GLOBAL:
            return f"{prefix}global:{variable.name}"
        elif variable.scope == VariableScope.PROJECT:
            return f"{prefix}project:{variable.project_id}:{variable.name}"
        elif variable.scope == VariableScope.ENVIRONMENT:
            return f"{prefix}env:{variable.environment_id}:{variable.name}"
        elif variable.scope == VariableScope.CASE:
            return f"{prefix}case:{variable.case_id}:{variable.name}"
        else:
            raise ValueError(f"不支持的变量作用域: {variable.scope}")

    @staticmethod
    def _build_variable_key_by_params(
            name: str,
            scope: VariableScope,
            project_id: Optional[int] = None,
            environment_id: Optional[int] = None,
            case_id: Optional[int] = None
    ) -> str:
        """
        根据参数构建变量Redis键
        
        :param name: 变量名
        :param scope: 变量作用域
        :param project_id: 项目ID
        :param environment_id: 环境ID
        :param case_id: 用例ID
        :return: Redis键
        """
        prefix = VariableManager.REDIS_KEY_PREFIX

        if scope == VariableScope.GLOBAL:
            return f"{prefix}global:{name}"
        elif scope == VariableScope.PROJECT:
            if not project_id:
                raise ValueError("项目变量需要指定project_id")
            return f"{prefix}project:{project_id}:{name}"
        elif scope == VariableScope.ENVIRONMENT:
            if not environment_id:
                raise ValueError("环境变量需要指定environment_id")
            return f"{prefix}env:{environment_id}:{name}"
        elif scope == VariableScope.CASE:
            if not case_id:
                raise ValueError("用例变量需要指定case_id")
            return f"{prefix}case:{case_id}:{name}"
        else:
            raise ValueError(f"不支持的变量作用域: {scope}")

    @staticmethod
    def _build_variable_key_pattern(
            scope: VariableScope,
            project_id: Optional[int] = None,
            environment_id: Optional[int] = None,
            case_id: Optional[int] = None
    ) -> str:
        """
        构建变量Redis键匹配模式
        
        :param scope: 变量作用域
        :param project_id: 项目ID
        :param environment_id: 环境ID
        :param case_id: 用例ID
        :return: Redis键匹配模式
        """
        prefix = VariableManager.REDIS_KEY_PREFIX

        if scope == VariableScope.GLOBAL:
            return f"{prefix}global:*"
        elif scope == VariableScope.PROJECT:
            if not project_id:
                raise ValueError("项目变量需要指定project_id")
            return f"{prefix}project:{project_id}:*"
        elif scope == VariableScope.ENVIRONMENT:
            if not environment_id:
                raise ValueError("环境变量需要指定environment_id")
            return f"{prefix}env:{environment_id}:*"
        elif scope == VariableScope.CASE:
            if not case_id:
                raise ValueError("用例变量需要指定case_id")
            return f"{prefix}case:{case_id}:*"
        else:
            raise ValueError(f"不支持的变量作用域: {scope}")

    @staticmethod
    def _encrypt_value(value: Any) -> str:
        """
        简单加密值（实际项目中应使用更安全的加密方法）
        
        :param value: 原始值
        :return: 加密后的值
        """
        # 这里仅作示例，实际应使用安全的加密算法
        if isinstance(value, str):
            import base64
            return f"encrypted:{base64.b64encode(value.encode()).decode()}"
        else:
            # 非字符串值先转为JSON字符串再加密
            import base64
            json_str = json.dumps(value)
            return f"encrypted:{base64.b64encode(json_str.encode()).decode()}"

    @staticmethod
    def _decrypt_value(value: str) -> Any:
        """
        简单解密值（实际项目中应使用更安全的解密方法）
        
        :param value: 加密后的值
        :return: 原始值
        """
        # 这里仅作示例，实际应使用安全的解密算法
        if not value.startswith("encrypted:"):
            return value

        encrypted_part = value[len("encrypted:"):]
        import base64
        decoded = base64.b64decode(encrypted_part).decode()

        try:
            # 尝试解析为JSON
            return json.loads(decoded)
        except:
            # 不是JSON，直接返回解密的字符串
            return decoded


class EnvironmentManager:
    """环境管理器"""

    # Redis键前缀
    REDIS_KEY_PREFIX = "api_testing:environment:"

    @classmethod
    async def create_environment(cls, environment: EnvironmentModel) -> bool:
        """
        创建环境
        
        :param environment: 环境信息
        :return: 是否成功
        """
        try:
            # 构建Redis键
            key = cls._build_environment_key(environment)

            # 存储环境信息
            await redis_client.set(key, environment.model_dump_json())

            # 如果设为默认环境，更新项目默认环境
            if environment.is_default:
                await cls.set_default_environment(environment.project_id, environment.id)

            return True
        except Exception as e:
            log.error(f"创建环境失败: {e}")
            return False

    @classmethod
    async def get_environment(cls, environment_id: int) -> Optional[EnvironmentModel]:
        """
        获取环境
        
        :param environment_id: 环境ID
        :return: 环境信息
        """
        try:
            # 构建Redis键
            key = f"{cls.REDIS_KEY_PREFIX}{environment_id}"

            # 获取环境信息
            data = await redis_client.get(key)
            if not data:
                return None

            # 解析环境信息
            return EnvironmentModel.model_validate_json(data)
        except Exception as e:
            log.error(f"获取环境失败: {e}")
            return None

    @classmethod
    async def update_environment(cls, environment: EnvironmentModel) -> bool:
        """
        更新环境
        
        :param environment: 环境信息
        :return: 是否成功
        """
        try:
            # 构建Redis键
            key = cls._build_environment_key(environment)

            # 检查环境是否存在
            exists = await redis_client.exists(key)
            if not exists:
                return False

            # 存储环境信息
            await redis_client.set(key, environment.model_dump_json())

            # 如果设为默认环境，更新项目默认环境
            if environment.is_default:
                await cls.set_default_environment(environment.project_id, environment.id)

            return True
        except Exception as e:
            log.error(f"更新环境失败: {e}")
            return False

    @classmethod
    async def delete_environment(cls, environment_id: int) -> bool:
        """
        删除环境
        
        :param environment_id: 环境ID
        :return: 是否成功
        """
        try:
            # 获取环境信息
            environment = await cls.get_environment(environment_id)
            if not environment:
                return False

            # 构建Redis键
            key = cls._build_environment_key(environment)

            # 删除环境信息
            await redis_client.delete(key)

            # 如果是默认环境，清除项目默认环境
            if environment.is_default:
                await cls.clear_default_environment(environment.project_id)

            return True
        except Exception as e:
            log.error(f"删除环境失败: {e}")
            return False

    @classmethod
    async def list_environments(cls, project_id: int) -> List[EnvironmentModel]:
        """
        获取项目环境列表
        
        :param project_id: 项目ID
        :return: 环境列表
        """
        try:
            # 构建Redis键模式
            pattern = f"{cls.REDIS_KEY_PREFIX}*"

            # 获取所有匹配的键
            keys = await redis_client.keys(pattern)

            environments = []
            for key in keys:
                data = await redis_client.get(key)
                if data:
                    env = EnvironmentModel.model_validate_json(data)
                    if env.project_id == project_id:
                        environments.append(env)

            return environments
        except Exception as e:
            log.error(f"获取环境列表失败: {e}")
            return []

    @classmethod
    async def get_default_environment(cls, project_id: int) -> Optional[EnvironmentModel]:
        """
        获取项目默认环境
        
        :param project_id: 项目ID
        :return: 默认环境信息
        """
        try:
            # 构建Redis键
            key = f"{cls.REDIS_KEY_PREFIX}default:{project_id}"
            # 获取默认环境ID
            environment_id = await redis_client.get(key)
            print("--->", environment_id)
            if not environment_id:
                return None

            # 获取环境信息
            return await cls.get_environment(int(environment_id))
        except Exception as e:
            log.error(f"获取默认环境失败: {e}")
            return None

    @classmethod
    async def set_default_environment(cls, project_id: int, environment_id: int) -> bool:
        """
        设置项目默认环境
        
        :param project_id: 项目ID
        :param environment_id: 环境ID
        :return: 是否成功
        """
        try:
            # 构建Redis键
            key = f"{cls.REDIS_KEY_PREFIX}default:{project_id}"

            # 设置默认环境ID
            await redis_client.set(key, str(environment_id))

            # 更新环境is_default标志
            await cls._update_environments_default_flag(project_id, environment_id)

            return True
        except Exception as e:
            log.error(f"设置默认环境失败: {e}")
            return False

    @classmethod
    async def clear_default_environment(cls, project_id: int) -> bool:
        """
        清除项目默认环境
        
        :param project_id: 项目ID
        :return: 是否成功
        """
        try:
            # 构建Redis键
            key = f"{cls.REDIS_KEY_PREFIX}default:{project_id}"

            # 删除默认环境记录
            await redis_client.delete(key)
            return True
        except Exception as e:
            log.error(f"清除默认环境失败: {e}")
            return False

    @classmethod
    async def _update_environments_default_flag(cls, project_id: int, default_environment_id: int) -> None:
        """
        更新项目环境的默认标志
        
        :param project_id: 项目ID
        :param default_environment_id: 默认环境ID
        """
        environments = await cls.list_environments(project_id)

        for env in environments:
            if env.id != default_environment_id and env.is_default:
                # 清除其他环境的默认标志
                env.is_default = False
                await cls.update_environment(env)
            elif env.id == default_environment_id and not env.is_default:
                # 设置指定环境为默认
                env.is_default = True
                await cls.update_environment(env)

    @staticmethod
    def _build_environment_key(environment: EnvironmentModel) -> str:
        """
        构建环境Redis键
        
        :param environment: 环境信息
        :return: Redis键
        """
        return f"{EnvironmentManager.REDIS_KEY_PREFIX}{environment.id}"
