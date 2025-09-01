#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from backend.common.enums import StatusType
from backend.common.model import Base


class ApiProject(Base):
    """API项目表"""
    __tablename__ = 'api_project'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    name = Column(String(64), nullable=False, comment='项目名称')
    description = Column(Text, nullable=True, comment='项目描述')
    base_url = Column(String(255), nullable=False, comment='基础URL')
    headers = Column(JSON, nullable=True, comment='全局请求头')
    variables = Column(JSON, nullable=True, comment='全局变量')
    status = Column(Integer, default=StatusType.enable.value, nullable=False, comment='状态 1启用 0禁用')

    # 关联关系
    test_cases: Mapped[List["ApiTestCase"]] = relationship("ApiTestCase", back_populates="project")


class ApiTestCase(Base):
    """API测试用例表"""
    __tablename__ = 'api_test_case'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    name = Column(String(64), nullable=False, comment='用例名称')
    project_id = Column(Integer, ForeignKey('api_project.id'), nullable=False, comment='所属项目ID')
    description = Column(Text, nullable=True, comment='用例描述')
    pre_script = Column(Text, nullable=True, comment='前置脚本')
    post_script = Column(Text, nullable=True, comment='后置脚本')
    status = Column(Integer, default=StatusType.enable.value, nullable=False, comment='状态 1启用 0禁用')

    # 关联关系
    project: Mapped["ApiProject"] = relationship("ApiProject", back_populates="test_cases")
    steps: Mapped[List["ApiTestStep"]] = relationship("ApiTestStep", back_populates="test_case")
    reports: Mapped[List["ApiTestReport"]] = relationship("ApiTestReport", back_populates="test_case")


class ApiTestStep(Base):
    """API测试步骤表"""
    __tablename__ = 'api_test_step'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    name = Column(String(64), nullable=False, comment='步骤名称')
    test_case_id = Column(Integer, ForeignKey('api_test_case.id'), nullable=False, comment='所属用例ID')
    url = Column(String(255), nullable=False, comment='请求URL')
    method = Column(String(16), nullable=False, comment='请求方法')
    headers = Column(JSON, nullable=True, comment='请求头')
    params = Column(JSON, nullable=True, comment='查询参数')
    body = Column(JSON, nullable=True, comment='请求体')
    files = Column(JSON, nullable=True, comment='上传文件')
    auth = Column(JSON, nullable=True, comment='认证信息')
    extract = Column(JSON, nullable=True, comment='提取变量')
    validate = Column(JSON, nullable=True, comment='断言列表')
    sql_queries = Column(JSON, nullable=True, comment='SQL查询列表')
    timeout = Column(Integer, default=30, nullable=False, comment='超时时间(秒)')
    retry = Column(Integer, default=0, nullable=False, comment='重试次数')
    retry_interval = Column(Integer, default=1, nullable=False, comment='重试间隔(秒)')
    order = Column(Integer, nullable=False, comment='步骤顺序')
    status = Column(Integer, default=StatusType.enable.value, nullable=False, comment='状态 1启用 0禁用')

    # 关联关系
    test_case: Mapped["ApiTestCase"] = relationship("ApiTestCase", back_populates="steps")


class ApiTestReport(Base):
    """API测试报告表"""
    __tablename__ = 'api_test_report'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    test_case_id = Column(Integer, ForeignKey('api_test_case.id'), nullable=False, comment='所属用例ID')
    name = Column(String(64), nullable=False, comment='报告名称')
    success = Column(Boolean, nullable=False, comment='是否成功')
    total_steps = Column(Integer, nullable=False, comment='总步骤数')
    success_steps = Column(Integer, nullable=False, comment='成功步骤数')
    fail_steps = Column(Integer, nullable=False, comment='失败步骤数')
    start_time = Column(DateTime, nullable=False, comment='开始时间')
    end_time = Column(DateTime, nullable=False, comment='结束时间')
    duration = Column(Integer, nullable=False, comment='执行时长(毫秒)')
    details = Column(JSON, nullable=False, comment='报告详情')

    # 关联关系
    test_case: Mapped["ApiTestCase"] = relationship("ApiTestCase", back_populates="reports")
