#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List
from sqlalchemy import String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.common.enums import StatusType
from backend.common.model import Base, id_key


class ApiProject(Base):
    """API项目表"""
    __tablename__ = 'api_project'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(64), comment='项目名称')
    base_url: Mapped[str] = mapped_column(String(255), comment='基础URL')
    headers: Mapped[dict | None] = mapped_column(JSON, default=None, comment='全局请求头')
    variables: Mapped[dict | None] = mapped_column(JSON, default=None, comment='全局变量')
    status: Mapped[int] = mapped_column(default=StatusType.enable.value, comment='状态 1启用 0禁用')
    description: Mapped[str | None] = mapped_column(Text, default=None, comment='项目描述')

    # 关联关系
    test_cases: Mapped[List["ApiTestCase"]] = relationship("ApiTestCase", back_populates="project", init=False)


class ApiTestCase(Base):
    """API测试用例表"""
    __tablename__ = 'api_test_case'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(64), comment='用例名称')
    project_id: Mapped[int] = mapped_column(ForeignKey('api_project.id'), comment='所属项目ID')
    description: Mapped[str | None] = mapped_column(Text, default=None, comment='用例描述')
    pre_script: Mapped[str | None] = mapped_column(Text, default=None, comment='前置脚本')
    post_script: Mapped[str | None] = mapped_column(Text, default=None, comment='后置脚本')
    status: Mapped[int] = mapped_column(default=StatusType.enable.value, comment='状态 1启用 0禁用')

    # 关联关系
    project: Mapped["ApiProject"] = relationship("ApiProject", back_populates="test_cases", init=False)
    steps: Mapped[List["ApiTestStep"]] = relationship("ApiTestStep", back_populates="test_case", init=False)
    reports: Mapped[List["ApiTestReport"]] = relationship("ApiTestReport", back_populates="test_case", init=False)


class ApiTestStep(Base):
    """API测试步骤表"""
    __tablename__ = 'api_test_step'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(64), comment='步骤名称')
    test_case_id: Mapped[int] = mapped_column(ForeignKey('api_test_case.id'), comment='所属用例ID')
    url: Mapped[str] = mapped_column(String(255), comment='请求URL')
    method: Mapped[str] = mapped_column(String(16), comment='请求方法')
    order: Mapped[int] = mapped_column(comment='步骤顺序')
    status: Mapped[int] = mapped_column(default=StatusType.enable.value, comment='状态 1启用 0禁用')
    headers: Mapped[dict | None] = mapped_column(JSON, default=None, comment='请求头')
    params: Mapped[dict | None] = mapped_column(JSON, default=None, comment='查询参数')
    body: Mapped[dict | None] = mapped_column(JSON, default=None, comment='请求体')
    files: Mapped[dict | None] = mapped_column(JSON, default=None, comment='上传文件')
    auth: Mapped[dict | None] = mapped_column(JSON, default=None, comment='认证信息')
    extract: Mapped[dict | None] = mapped_column(JSON, default=None, comment='提取变量')
    validate: Mapped[dict | None] = mapped_column(JSON, default=None, comment='断言列表')
    sql_queries: Mapped[dict | None] = mapped_column(JSON, default=None, comment='SQL查询列表')
    timeout: Mapped[int] = mapped_column(default=30, comment='超时时间(秒)')
    retry: Mapped[int] = mapped_column(default=0, comment='重试次数')
    retry_interval: Mapped[int] = mapped_column(default=1, comment='重试间隔(秒)')

    # 关联关系
    test_case: Mapped["ApiTestCase"] = relationship("ApiTestCase", back_populates="steps", init=False)


class ApiTestReport(Base):
    """API测试报告表"""
    __tablename__ = 'api_test_report'

    id: Mapped[id_key] = mapped_column(init=False)
    test_case_id: Mapped[int] = mapped_column(ForeignKey('api_test_case.id'), comment='所属用例ID')
    name: Mapped[str] = mapped_column(String(64), comment='报告名称')
    success: Mapped[bool] = mapped_column(Boolean, comment='是否成功')
    total_steps: Mapped[int] = mapped_column(comment='总步骤数')
    success_steps: Mapped[int] = mapped_column(comment='成功步骤数')
    fail_steps: Mapped[int] = mapped_column(comment='失败步骤数')
    start_time: Mapped[datetime] = mapped_column(DateTime, comment='开始时间')
    end_time: Mapped[datetime] = mapped_column(DateTime, comment='结束时间')
    duration: Mapped[int] = mapped_column(comment='执行时长(毫秒)')
    details: Mapped[dict] = mapped_column(JSON, comment='报告详情')

    # 关联关系
    test_case: Mapped["ApiTestCase"] = relationship("ApiTestCase", back_populates="reports", init=False)
