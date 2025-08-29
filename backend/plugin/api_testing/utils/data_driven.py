#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据驱动测试工具
提供数据驱动测试支持
"""
import csv
import json
import os
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from pydantic import BaseModel, Field
from backend.common.log import log
from backend.core.path_conf import PLUGIN_DIR

# 尝试导入可选依赖
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    log.warning("pandas库未安装，Excel数据源功能将不可用。")

try:
    import xlrd
    XLRD_AVAILABLE = True
except ImportError:
    XLRD_AVAILABLE = False
    log.warning("xlrd库未安装，Excel数据源功能将不可用。")


class DataSourceType(str, Enum):
    """数据源类型枚举"""
    CSV = "csv"  # CSV文件
    EXCEL = "excel"  # Excel文件
    JSON = "json"  # JSON文件
    DATABASE = "database"  # 数据库
    PARAMETER = "parameter"  # 直接参数


class DatabaseType(str, Enum):
    """数据库类型枚举"""
    MYSQL = "mysql"  # MySQL
    POSTGRESQL = "postgresql"  # PostgreSQL
    SQLITE = "sqlite"  # SQLite


class DataSourceConfig(BaseModel):
    """数据源配置"""
    name: str  # 数据源名称
    type: DataSourceType  # 数据源类型
    file_path: Optional[str] = None  # 文件路径，用于文件类型的数据源
    sheet_name: Optional[str] = None  # Excel表格名，用于Excel类型的数据源
    database_type: Optional[DatabaseType] = None  # 数据库类型，用于数据库类型的数据源
    database_config: Optional[Dict[str, Any]] = None  # 数据库配置，用于数据库类型的数据源
    sql: Optional[str] = None  # SQL查询，用于数据库类型的数据源
    parameters: Optional[List[Dict[str, Any]]] = None  # 参数列表，用于参数类型的数据源
    description: Optional[str] = None  # 数据源描述


class TestCaseParameter(BaseModel):
    """测试用例参数"""
    name: str  # 参数名
    value: Any  # 参数值
    description: Optional[str] = None  # 参数描述


class TestIteration(BaseModel):
    """测试迭代数据"""
    id: str  # 迭代ID
    parameters: Dict[str, Any]  # 参数字典
    description: Optional[str] = None  # 迭代描述


class LoopMode(str, Enum):
    """循环模式枚举"""
    SEQUENTIAL = "sequential"  # 顺序执行
    RANDOM = "random"  # 随机执行
    PARALLEL = "parallel"  # 并行执行


class DataDrivenConfig(BaseModel):
    """数据驱动测试配置"""
    enabled: bool = False  # 是否启用数据驱动测试
    data_source: Optional[DataSourceConfig] = None  # 数据源配置
    parameters: List[TestCaseParameter] = []  # 测试参数列表
    iterations: List[TestIteration] = []  # 测试迭代数据列表
    loop_mode: LoopMode = LoopMode.SEQUENTIAL  # 循环模式
    max_iterations: Optional[int] = None  # 最大迭代次数
    skip_failed: bool = False  # 失败时是否跳过
    stop_on_fail: bool = False  # 失败时是否停止


class DataDriverManager:
    """数据驱动测试管理器"""
    
    @classmethod
    async def load_data_source(cls, config: DataSourceConfig) -> List[Dict[str, Any]]:
        """
        加载数据源
        
        :param config: 数据源配置
        :return: 数据列表
        """
        try:
            if config.type == DataSourceType.CSV:
                return cls._load_csv_data(config)
            elif config.type == DataSourceType.EXCEL:
                if not PANDAS_AVAILABLE or not XLRD_AVAILABLE:
                    raise ImportError("Excel数据源需要pandas和xlrd库支持")
                return cls._load_excel_data(config)
            elif config.type == DataSourceType.JSON:
                return cls._load_json_data(config)
            elif config.type == DataSourceType.DATABASE:
                return await cls._load_database_data(config)
            elif config.type == DataSourceType.PARAMETER:
                return cls._load_parameter_data(config)
            else:
                log.error(f"不支持的数据源类型: {config.type}")
                return []
        except Exception as e:
            log.error(f"加载数据源失败: {e}")
            return []
    
    @classmethod
    async def prepare_iterations(cls, config: DataDrivenConfig) -> List[TestIteration]:
        """
        准备测试迭代数据
        
        :param config: 数据驱动测试配置
        :return: 测试迭代数据列表
        """
        try:
            # 如果已有迭代数据，则直接返回
            if config.iterations:
                return config.iterations
                
            # 如果没有数据源配置，则返回空列表
            if not config.data_source:
                return []
                
            # 加载数据源
            data_list = await cls.load_data_source(config.data_source)
            if not data_list:
                return []
                
            # 限制迭代次数
            if config.max_iterations and len(data_list) > config.max_iterations:
                data_list = data_list[:config.max_iterations]
                
            # 生成迭代数据
            iterations = []
            for index, data in enumerate(data_list):
                # 构建参数字典
                parameters = {}
                for param in config.parameters:
                    if param.name in data:
                        parameters[param.name] = data[param.name]
                    else:
                        # 如果数据中没有对应的参数，则使用默认值
                        parameters[param.name] = param.value
                        
                # 创建迭代数据
                iteration = TestIteration(
                    id=f"iter_{index + 1}",
                    parameters=parameters,
                    description=f"Iteration {index + 1}"
                )
                iterations.append(iteration)
                
            return iterations
        except Exception as e:
            log.error(f"准备测试迭代数据失败: {e}")
            return []
    
    @staticmethod
    def _load_csv_data(config: DataSourceConfig) -> List[Dict[str, Any]]:
        """
        加载CSV数据
        
        :param config: 数据源配置
        :return: 数据列表
        """
        if not config.file_path:
            raise ValueError("CSV数据源需要指定文件路径")
            
        file_path = config.file_path
        if not os.path.isabs(file_path):
            # 如果是相对路径，则相对于插件目录
            file_path = os.path.join(PLUGIN_DIR, 'api_testing', file_path)
            
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV文件不存在: {file_path}")
            
        # 读取CSV文件
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            
        return data
    
    @staticmethod
    def _load_excel_data(config: DataSourceConfig) -> List[Dict[str, Any]]:
        """
        加载Excel数据
        
        :param config: 数据源配置
        :return: 数据列表
        """
        if not PANDAS_AVAILABLE or not XLRD_AVAILABLE:
            raise ImportError("Excel数据源需要pandas和xlrd库支持")
            
        if not config.file_path:
            raise ValueError("Excel数据源需要指定文件路径")
            
        file_path = config.file_path
        if not os.path.isabs(file_path):
            # 如果是相对路径，则相对于插件目录
            file_path = os.path.join(PLUGIN_DIR, 'api_testing', file_path)
            
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel文件不存在: {file_path}")
            
        # 读取Excel文件
        df = pd.read_excel(file_path, sheet_name=config.sheet_name)
        data = df.to_dict(orient='records')
            
        return data
    
    @staticmethod
    def _load_json_data(config: DataSourceConfig) -> List[Dict[str, Any]]:
        """
        加载JSON数据
        
        :param config: 数据源配置
        :return: 数据列表
        """
        if not config.file_path:
            raise ValueError("JSON数据源需要指定文件路径")
            
        file_path = config.file_path
        if not os.path.isabs(file_path):
            # 如果是相对路径，则相对于插件目录
            file_path = os.path.join(PLUGIN_DIR, 'api_testing', file_path)
            
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"JSON文件不存在: {file_path}")
            
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 如果数据不是列表，则转换为列表
        if not isinstance(data, list):
            data = [data]
            
        return data
    
    @staticmethod
    async def _load_database_data(config: DataSourceConfig) -> List[Dict[str, Any]]:
        """
        加载数据库数据
        
        :param config: 数据源配置
        :return: 数据列表
        """
        if not config.database_type:
            raise ValueError("数据库数据源需要指定数据库类型")
        if not config.database_config:
            raise ValueError("数据库数据源需要指定数据库配置")
        if not config.sql:
            raise ValueError("数据库数据源需要指定SQL查询")
            
        # 根据数据库类型选择不同的连接方式
        if config.database_type == DatabaseType.MYSQL:
            try:
                import pymysql
            except ImportError:
                raise ImportError("MySQL数据源需要pymysql库支持")
                
            # 获取数据库配置
            db_config = config.database_config
            if 'host' not in db_config or 'user' not in db_config or 'password' not in db_config or 'database' not in db_config:
                raise ValueError("MySQL数据库配置不完整，需要指定host、user、password、database")
                
            # 连接数据库
            connection = pymysql.connect(
                host=db_config.get('host'),
                user=db_config.get('user'),
                password=db_config.get('password'),
                database=db_config.get('database'),
                port=db_config.get('port', 3306),
                charset=db_config.get('charset', 'utf8mb4'),
                cursorclass=pymysql.cursors.DictCursor
            )
            
            try:
                cursor = connection.cursor()
                cursor.execute(config.sql)
                data = cursor.fetchall()
                return list(data)
            finally:
                connection.close()
        elif config.database_type == DatabaseType.POSTGRESQL:
            try:
                import psycopg2
                import psycopg2.extras
            except ImportError:
                raise ImportError("PostgreSQL数据源需要psycopg2库支持")
            
            # 获取数据库配置
            db_config = config.database_config
            if 'host' not in db_config or 'user' not in db_config or 'password' not in db_config or 'database' not in db_config:
                raise ValueError("PostgreSQL数据库配置不完整，需要指定host、user、password、database")
                
            # 构建连接字符串
            conn_str = f"host={db_config.get('host')} port={db_config.get('port', 5432)} user={db_config.get('user')} password={db_config.get('password')} dbname={db_config.get('database')}"
            
            # 连接数据库
            connection = psycopg2.connect(conn_str)
            try:
                cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute(config.sql)
                data = cursor.fetchall()
                return [dict(row) for row in data]
            finally:
                connection.close()
        elif config.database_type == DatabaseType.SQLITE:
            try:
                import sqlite3
            except ImportError:
                raise ImportError("SQLite数据源需要sqlite3库支持")
            
            # 获取数据库配置
            db_config = config.database_config
            if 'database' not in db_config:
                raise ValueError("SQLite数据库配置不完整，需要指定database")
                
            # 数据库文件路径
            db_path = db_config.get('database')
            if not os.path.isabs(db_path):
                # 如果是相对路径，则相对于插件目录
                db_path = os.path.join(PLUGIN_DIR, 'api_testing', db_path)
                
            # 连接数据库
            connection = sqlite3.connect(db_path)
            try:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute(config.sql)
                data = cursor.fetchall()
                return [dict(row) for row in data]
            finally:
                connection.close()
        else:
            raise ValueError(f"不支持的数据库类型: {config.database_type}")
    
    @staticmethod
    def _load_parameter_data(config: DataSourceConfig) -> List[Dict[str, Any]]:
        """
        加载参数数据
        
        :param config: 数据源配置
        :return: 数据列表
        """
        if not config.parameters:
            raise ValueError("参数数据源需要指定参数列表")
            
        return config.parameters