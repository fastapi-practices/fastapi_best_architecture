#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版测试报告生成工具
支持生成包含失败分析的详细HTML和JSON格式测试报告
"""
import json
import os
import re
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import jinja2
from pydantic import BaseModel

from backend.core.path_conf import PLUGIN_DIR
from backend.plugin.api_testing.utils.failure_analyzer import FailureAnalysisResult, FailureAnalyzer
from backend.plugin.api_testing.utils.http_client import RequestResult
from backend.plugin.api_testing.utils.report_generator import ReportFormat, StepResult, TestReport


class EnhancedStepResult(StepResult):
    """增强版测试步骤结果"""
    failure_analysis: Optional[FailureAnalysisResult] = None  # 失败分析结果
    curl_command: Optional[str] = None  # cURL命令


class EnhancedTestReport(TestReport):
    """增强版测试报告数据模型"""
    steps: List[EnhancedStepResult]  # 重写步骤结果类型
    has_analysis: bool = True  # 是否包含失败分析


class EnhancedReportGenerator:
    """增强版报告生成器"""
    
    def __init__(self):
        """初始化报告生成器"""
        self.template_dir = os.path.join(PLUGIN_DIR, 'api_testing', 'report_templates')
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=True
        )
    
    def generate_report(self, report_data: EnhancedTestReport, format: ReportFormat = ReportFormat.HTML) -> str:
        """
        生成测试报告
        
        :param report_data: 报告数据
        :param format: 报告格式
        :return: 报告内容
        """
        # 添加失败分析
        self._add_failure_analysis(report_data)
        
        # 添加cURL命令
        self._add_curl_commands(report_data)
        
        if format == ReportFormat.HTML:
            return self._generate_html_report(report_data)
        elif format == ReportFormat.JSON:
            return self._generate_json_report(report_data)
        else:
            raise ValueError(f"不支持的报告格式: {format}")
    
    def _add_failure_analysis(self, report_data: EnhancedTestReport) -> None:
        """
        为失败步骤添加失败分析
        
        :param report_data: 报告数据
        """
        for step in report_data.steps:
            if not step.success:
                step_dict = step.model_dump()
                analysis = FailureAnalyzer.analyze_step_failure(step_dict)
                step.failure_analysis = analysis
    
    def _add_curl_commands(self, report_data: EnhancedTestReport) -> None:
        """
        为每个步骤添加cURL命令
        
        :param report_data: 报告数据
        """
        for step in report_data.steps:
            curl_cmd = self._generate_curl_command(step)
            step.curl_command = curl_cmd
    
    def _generate_curl_command(self, step: EnhancedStepResult) -> str:
        """
        生成cURL命令
        
        :param step: 步骤结果
        :return: cURL命令
        """
        url = step.url
        method = step.method.upper()
        curl = [f'curl -X {method}']
        
        # 添加请求头
        headers = step.request_data.get('headers', {})
        for key, value in headers.items():
            curl.append(f"-H '{key}: {value}'")
        
        # 添加请求体
        if step.request_data.get('json_data'):
            curl.append("-H 'Content-Type: application/json'")
            json_data = json.dumps(step.request_data.get('json_data'))
            curl.append(f"-d '{json_data}'")
        elif step.request_data.get('data'):
            data_items = []
            for key, value in step.request_data.get('data', {}).items():
                data_items.append(f"{key}={value}")
            curl.append(f"-d '{('&').join(data_items)}'")
        
        # 添加查询参数
        if step.request_data.get('params'):
            params = []
            for key, value in step.request_data.get('params', {}).items():
                params.append(f"{key}={value}")
            if '?' in url:
                url += '&' + ('&').join(params)
            else:
                url += '?' + ('&').join(params)
        
        # 添加URL
        curl.append(f"'{url}'")
        
        return ' \\\n  '.join(curl)
    
    def _generate_html_report(self, report_data: EnhancedTestReport) -> str:
        """
        生成HTML格式的测试报告
        
        :param report_data: 报告数据
        :return: HTML报告内容
        """
        try:
            template = self.env.get_template('enhanced_report_template.html')
            return template.render(
                report=report_data,
                current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        except jinja2.exceptions.TemplateNotFound:
            # 如果模板不存在，直接抛出异常，用户需要确保enhanced_report_template.html已创建
            raise ValueError("增强版报告模板不存在，请确保enhanced_report_template.html文件已创建")
    
    def _generate_json_report(self, report_data: EnhancedTestReport) -> str:
        """
        生成JSON格式的测试报告
        
        :param report_data: 报告数据
        :return: JSON报告内容
        """
        # 将报告对象转换为字典
        report_dict = report_data.model_dump()
        
        # 处理日期时间字段
        report_dict['start_time'] = report_dict['start_time'].isoformat()
        report_dict['end_time'] = report_dict['end_time'].isoformat()
        
        for step in report_dict['steps']:
            step['start_time'] = step['start_time'].isoformat()
            step['end_time'] = step['end_time'].isoformat()
        
        # 转换为JSON字符串
        return json.dumps(report_dict, ensure_ascii=False, indent=2)


# 创建增强版报告生成器单例
enhanced_report_generator = EnhancedReportGenerator()