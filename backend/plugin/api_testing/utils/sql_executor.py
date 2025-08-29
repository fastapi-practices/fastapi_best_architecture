#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL执行工具模块
提供数据库查询和执行功能
"""
import pymysql
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from backend.common.log import log
from backend.core.conf import settings


# 尝试导入psycopg，如果失败则提供兼容性处理
try:
    import psycopg
    PSYCOPG_AVAILABLE = True
except ImportError:
    PSYCOPG_AVAILABLE = False
    log.warning("psycopg库未安装或缺少PostgreSQL客户端库，PostgreSQL功能将不可用。")


class DatabaseType(str, Enum):
    """数据库类型枚举"""
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"


class DBConfig(BaseModel):
    """数据库配置"""
    type: DatabaseType
    host: str
    port: int
    username: str
    password: str
    database: str


class SQLQuery(BaseModel):
    """SQL查询配置"""
    name: str  # 查询名称
    query: str  # SQL查询语句
    extract: Optional[Dict[str, str]] = None  # 提取变量配置
    validations: Optional[List[Dict[str, Any]]] = None  # 断言配置
    use_default_db: bool = True  # 是否使用默认数据库配置
    db_config: Optional[DBConfig] = None  # 数据库配置


class SQLResult(BaseModel):
    """SQL执行结果"""
    name: str  # 查询名称
    query: str  # 执行的SQL语句
    success: bool  # 是否成功
    error: Optional[str] = None  # 错误信息
    data: Optional[List[Dict[str, Any]]] = None  # 查询结果
    affected_rows: Optional[int] = None  # 影响的行数
    extracted_variables: Optional[Dict[str, Any]] = None  # 提取的变量


class SQLExecutor:
    """SQL执行器"""
    
    @staticmethod
    def get_default_db_config() -> DBConfig:
        """
        获取默认数据库配置
        
        :return: 数据库配置
        """
        db_type = DatabaseType.MYSQL if settings.DATABASE_TYPE == "mysql" else DatabaseType.POSTGRESQL
        
        return DBConfig(
            type=db_type,
            host=settings.DATABASE_HOST,
            port=settings.DATABASE_PORT,
            username=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            database=settings.DATABASE_SCHEMA
        )
    
    @staticmethod
    async def execute_query(sql_query: SQLQuery) -> SQLResult:
        """
        执行SQL查询
        
        :param sql_query: SQL查询配置
        :return: 查询结果
        """
        # 获取数据库配置
        db_config = sql_query.db_config
        if sql_query.use_default_db or db_config is None:
            db_config = SQLExecutor.get_default_db_config()
        
        # 初始化结果
        result = SQLResult(
            name=sql_query.name,
            query=sql_query.query,
            success=False
        )
        
        # 根据数据库类型选择连接方式
        try:
            if db_config.type == DatabaseType.MYSQL:
                return await SQLExecutor._execute_mysql_query(sql_query, db_config, result)
            elif db_config.type == DatabaseType.POSTGRESQL:
                # 检查是否支持PostgreSQL
                if not PSYCOPG_AVAILABLE:
                    result.error = "PostgreSQL功能不可用，请安装psycopg及PostgreSQL客户端库"
                    return result
                return await SQLExecutor._execute_postgresql_query(sql_query, db_config, result)
            else:
                result.error = f"不支持的数据库类型: {db_config.type}"
                return result
        except Exception as e:
            result.error = f"SQL执行异常: {str(e)}"
            log.error(f"SQL执行异常: {str(e)}")
            return result
    
    @staticmethod
    async def _execute_mysql_query(sql_query: SQLQuery, db_config: DBConfig, result: SQLResult) -> SQLResult:
        """
        执行MySQL查询
        
        :param sql_query: SQL查询配置
        :param db_config: 数据库配置
        :param result: 结果对象
        :return: 查询结果
        """
        connection = None
        cursor = None
        
        try:
            # 连接数据库
            connection = pymysql.connect(
                host=db_config.host,
                port=db_config.port,
                user=db_config.username,
                password=db_config.password,
                database=db_config.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor  # 返回字典格式的结果
            )
            
            cursor = connection.cursor()
            
            # 执行查询
            affected_rows = cursor.execute(sql_query.query)
            result.affected_rows = affected_rows
            
            # 如果是SELECT查询，获取结果
            if sql_query.query.strip().upper().startswith('SELECT'):
                data = cursor.fetchall()
                result.data = [dict(row) for row in data]
            
            # 提交事务
            connection.commit()
            result.success = True
            
            # 提取变量
            if sql_query.extract and result.data:
                result.extracted_variables = SQLExecutor._extract_variables(sql_query.extract, result.data)
            
            return result
            
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    async def _execute_postgresql_query(sql_query: SQLQuery, db_config: DBConfig, result: SQLResult) -> SQLResult:
        """
        执行PostgreSQL查询
        
        :param sql_query: SQL查询配置
        :param db_config: 数据库配置
        :param result: 结果对象
        :return: 查询结果
        """
        # 由于已经在execute_query中检查了PSYCOPG_AVAILABLE，此处可以安全使用psycopg
        connection = None
        cursor = None
        
        try:
            # 构建连接字符串
            conn_str = f"postgresql://{db_config.username}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}"
            
            # 连接数据库
            connection = psycopg.connect(conn_str)
            
            cursor = connection.cursor(row_factory=psycopg.rows.dict_row)  # 返回字典格式的结果
            
            # 执行查询
            cursor.execute(sql_query.query)
            
            # 如果是SELECT查询，获取结果
            if sql_query.query.strip().upper().startswith('SELECT'):
                data = cursor.fetchall()
                result.data = [dict(row) for row in data]
                result.affected_rows = len(data)
            else:
                result.affected_rows = cursor.rowcount
            
            # 提交事务
            connection.commit()
            result.success = True
            
            # 提取变量
            if sql_query.extract and result.data:
                result.extracted_variables = SQLExecutor._extract_variables(sql_query.extract, result.data)
            
            return result
            
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def _extract_variables(extract_config: Dict[str, str], data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        从查询结果中提取变量
        
        :param extract_config: 提取配置，格式为 {"变量名": "提取表达式"}
        :param data: 查询结果数据
        :return: 提取的变量字典
        """
        variables = {}
        
        for var_name, expr in extract_config.items():
            # 支持简单的表达式，例如 "0.id" 表示第一行的id字段
            parts = expr.split('.')
            
            try:
                if len(parts) >= 2:
                    # 获取行索引
                    row_idx = int(parts[0])
                    if row_idx < len(data):
                        # 获取字段
                        field = '.'.join(parts[1:])
                        if field in data[row_idx]:
                            variables[var_name] = data[row_idx][field]
            except (ValueError, IndexError):
                pass
        
        return variables