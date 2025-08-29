#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试报告生成工具
支持生成HTML和JSON格式的测试报告
"""
import jinja2
import json
import os
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from backend.core.path_conf import PLUGIN_DIR


class ReportFormat(str, Enum):
    """报告格式枚举"""
    HTML = "html"
    JSON = "json"


class StepResult(BaseModel):
    """测试步骤结果"""
    name: str  # 步骤名称
    order: int  # 步骤顺序
    url: str  # 请求URL
    method: str  # 请求方法
    request_data: Dict[str, Any]  # 请求数据
    response: Dict[str, Any]  # 响应数据
    assertions: List[Dict[str, Any]]  # 断言结果
    sql_results: Optional[List[Dict[str, Any]]] = None  # SQL执行结果
    variables: Optional[Dict[str, Any]] = None  # 提取的变量
    success: bool  # 步骤是否成功
    start_time: datetime  # 开始时间
    end_time: datetime  # 结束时间
    duration: int  # 执行时长(毫秒)


class TestReport(BaseModel):
    """测试报告数据模型"""
    name: str  # 报告名称
    project_name: str  # 项目名称
    test_case_name: str  # 测试用例名称
    description: Optional[str] = None  # 报告描述
    environment: Optional[str] = None  # 测试环境
    success: bool  # 是否成功
    total_steps: int  # 总步骤数
    success_steps: int  # 成功步骤数
    fail_steps: int  # 失败步骤数
    steps: List[StepResult]  # 步骤结果
    start_time: datetime  # 开始时间
    end_time: datetime  # 结束时间
    duration: int  # 执行时长(毫秒)


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self):
        """初始化报告生成器"""
        self.template_dir = os.path.join(PLUGIN_DIR, 'api_testing', 'report_templates')
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=True
        )
    
    def generate_report(self, report_data: TestReport, format: ReportFormat = ReportFormat.HTML) -> str:
        """
        生成测试报告
        
        :param report_data: 报告数据
        :param format: 报告格式
        :return: 报告内容
        """
        if format == ReportFormat.HTML:
            return self._generate_html_report(report_data)
        elif format == ReportFormat.JSON:
            return self._generate_json_report(report_data)
        else:
            raise ValueError(f"不支持的报告格式: {format}")
    
    def _generate_html_report(self, report_data: TestReport) -> str:
        """
        生成HTML格式的测试报告
        
        :param report_data: 报告数据
        :return: HTML报告内容
        """
        try:
            template = self.env.get_template('report_template.html')
            return template.render(
                report=report_data,
                current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        except jinja2.exceptions.TemplateNotFound:
            # 如果模板不存在，先创建默认模板
            self._create_default_html_template()
            template = self.env.get_template('report_template.html')
            return template.render(
                report=report_data,
                current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
    
    def _generate_json_report(self, report_data: TestReport) -> str:
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
    
    def _create_default_html_template(self) -> None:
        """创建默认HTML报告模板"""
        # 确保模板目录存在
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
        
        # 默认HTML模板
        template_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ report.name }} - 接口自动化测试报告</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .report-header {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,.1);
            margin-bottom: 20px;
        }
        .report-title {
            margin: 0;
            color: #333;
        }
        .report-meta {
            display: flex;
            flex-wrap: wrap;
            margin-top: 15px;
        }
        .meta-item {
            flex: 1;
            min-width: 200px;
            margin-bottom: 10px;
        }
        .meta-label {
            font-weight: bold;
            color: #666;
        }
        .summary {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,.1);
            margin-bottom: 20px;
        }
        .summary-title {
            margin-top: 0;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
            color: #333;
        }
        .summary-data {
            display: flex;
            flex-wrap: wrap;
            text-align: center;
        }
        .summary-item {
            flex: 1;
            min-width: 120px;
            padding: 15px;
        }
        .summary-value {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .success-value { color: #28a745; }
        .fail-value { color: #dc3545; }
        .summary-label {
            color: #666;
        }
        .steps {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,.1);
        }
        .steps-title {
            margin-top: 0;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
            color: #333;
        }
        .step-item {
            border-bottom: 1px solid #eee;
            padding: 15px 0;
        }
        .step-item:last-child {
            border-bottom: none;
        }
        .step-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }
        .step-name {
            font-weight: bold;
            font-size: 18px;
            margin: 0;
        }
        .step-status {
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        .status-success {
            background-color: #d4edda;
            color: #28a745;
        }
        .status-fail {
            background-color: #f8d7da;
            color: #dc3545;
        }
        .step-content {
            display: none;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            margin-top: 10px;
        }
        .step-section {
            margin-bottom: 15px;
        }
        .step-section-title {
            font-weight: bold;
            margin-bottom: 5px;
            color: #495057;
        }
        .request-url {
            background-color: #e9ecef;
            padding: 10px;
            border-radius: 4px;
            font-family: monospace;
            word-break: break-all;
        }
        .code-block {
            background-color: #e9ecef;
            padding: 10px;
            border-radius: 4px;
            font-family: monospace;
            white-space: pre-wrap;
            word-break: break-all;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border: 1px solid #dee2e6;
        }
        th {
            background-color: #f2f2f2;
        }
        .badge {
            padding: 3px 6px;
            border-radius: 3px;
            font-size: 12px;
        }
        .badge-success {
            background-color: #d4edda;
            color: #28a745;
        }
        .badge-danger {
            background-color: #f8d7da;
            color: #dc3545;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            font-size: 14px;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="report-header">
        <h1 class="report-title">{{ report.name }}</h1>
        <div class="report-meta">
            <div class="meta-item">
                <div class="meta-label">项目名称:</div>
                <div>{{ report.project_name }}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">测试用例:</div>
                <div>{{ report.test_case_name }}</div>
            </div>
            {% if report.environment %}
            <div class="meta-item">
                <div class="meta-label">测试环境:</div>
                <div>{{ report.environment }}</div>
            </div>
            {% endif %}
            <div class="meta-item">
                <div class="meta-label">开始时间:</div>
                <div>{{ report.start_time.strftime('%Y-%m-%d %H:%M:%S') }}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">结束时间:</div>
                <div>{{ report.end_time.strftime('%Y-%m-%d %H:%M:%S') }}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">总耗时:</div>
                <div>{{ '{:.2f}'.format(report.duration / 1000) }} 秒</div>
            </div>
        </div>
    </div>

    <div class="summary">
        <h2 class="summary-title">测试摘要</h2>
        <div class="summary-data">
            <div class="summary-item">
                <div class="summary-value">{{ report.total_steps }}</div>
                <div class="summary-label">总步骤</div>
            </div>
            <div class="summary-item">
                <div class="summary-value success-value">{{ report.success_steps }}</div>
                <div class="summary-label">成功</div>
            </div>
            <div class="summary-item">
                <div class="summary-value fail-value">{{ report.fail_steps }}</div>
                <div class="summary-label">失败</div>
            </div>
            <div class="summary-item">
                <div class="summary-value {% if report.success %}success-value{% else %}fail-value{% endif %}">
                    {{ '{:.0%}'.format(report.success_steps / report.total_steps) if report.total_steps > 0 else '0%' }}
                </div>
                <div class="summary-label">通过率</div>
            </div>
        </div>
    </div>

    <div class="steps">
        <h2 class="steps-title">测试步骤详情</h2>
        {% for step in report.steps %}
        <div class="step-item">
            <div class="step-header" onclick="toggleStepContent('step-{{ loop.index }}')">
                <h3 class="step-name">{{ step.order }}. {{ step.name }}</h3>
                <span class="step-status {% if step.success %}status-success{% else %}status-fail{% endif %}">
                    {% if step.success %}成功{% else %}失败{% endif %}
                </span>
            </div>
            <div class="step-content" id="step-{{ loop.index }}">
                <div class="step-section">
                    <div class="step-section-title">请求信息</div>
                    <div class="request-url">{{ step.method }} {{ step.url }}</div>
                    
                    <h4>请求头</h4>
                    {% if step.request_data.headers %}
                    <table>
                        <thead>
                            <tr>
                                <th>名称</th>
                                <th>值</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for key, value in step.request_data.headers.items() %}
                            <tr>
                                <td>{{ key }}</td>
                                <td>{{ value }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    {% else %}
                    <p>无</p>
                    {% endif %}
                    
                    {% if step.request_data.params %}
                    <h4>查询参数</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>名称</th>
                                <th>值</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for key, value in step.request_data.params.items() %}
                            <tr>
                                <td>{{ key }}</td>
                                <td>{{ value }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    {% endif %}
                    
                    {% if step.request_data.json_data %}
                    <h4>请求体 (JSON)</h4>
                    <div class="code-block">{{ step.request_data.json_data | tojson(indent=2) }}</div>
                    {% elif step.request_data.data %}
                    <h4>请求体 (表单)</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>名称</th>
                                <th>值</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for key, value in step.request_data.data.items() %}
                            <tr>
                                <td>{{ key }}</td>
                                <td>{{ value }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    {% endif %}
                </div>
                
                <div class="step-section">
                    <div class="step-section-title">响应信息</div>
                    <table>
                        <tr>
                            <td>状态码</td>
                            <td>{{ step.response.status_code }}</td>
                        </tr>
                        <tr>
                            <td>响应时间</td>
                            <td>{{ '{:.2f}'.format(step.response.elapsed_time) }} 毫秒</td>
                        </tr>
                    </table>
                    
                    <h4>响应头</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>名称</th>
                                <th>值</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for key, value in step.response.headers.items() %}
                            <tr>
                                <td>{{ key }}</td>
                                <td>{{ value }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    
                    {% if step.response.json_data %}
                    <h4>响应体 (JSON)</h4>
                    <div class="code-block">{{ step.response.json_data | tojson(indent=2) }}</div>
                    {% else %}
                    <h4>响应体</h4>
                    <div class="code-block">{{ step.response.text }}</div>
                    {% endif %}
                </div>
                
                {% if step.assertions %}
                <div class="step-section">
                    <div class="step-section-title">断言结果</div>
                    <table>
                        <thead>
                            <tr>
                                <th>断言类型</th>
                                <th>路径</th>
                                <th>预期值</th>
                                <th>实际值</th>
                                <th>结果</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for assertion in step.assertions %}
                            <tr>
                                <td>{{ assertion.assertion.type }}</td>
                                <td>{{ assertion.assertion.path if assertion.assertion.path else '-' }}</td>
                                <td>{{ assertion.assertion.expected if assertion.assertion.expected is not none else '-' }}</td>
                                <td>{{ assertion.actual if assertion.actual is not none else '-' }}</td>
                                <td>
                                    <span class="badge {% if assertion.success %}badge-success{% else %}badge-danger{% endif %}">
                                        {% if assertion.success %}通过{% else %}失败{% endif %}
                                    </span>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% endif %}
                
                {% if step.sql_results %}
                <div class="step-section">
                    <div class="step-section-title">SQL执行结果</div>
                    {% for sql_result in step.sql_results %}
                    <div style="margin-bottom: 20px;">
                        <h4>{{ sql_result.name }}</h4>
                        <div class="code-block">{{ sql_result.query }}</div>
                        
                        <p>
                            状态: 
                            <span class="badge {% if sql_result.success %}badge-success{% else %}badge-danger{% endif %}">
                                {% if sql_result.success %}成功{% else %}失败{% endif %}
                            </span>
                        </p>
                        
                        {% if sql_result.error %}
                        <p>错误信息: {{ sql_result.error }}</p>
                        {% endif %}
                        
                        {% if sql_result.affected_rows is not none %}
                        <p>影响行数: {{ sql_result.affected_rows }}</p>
                        {% endif %}
                        
                        {% if sql_result.data %}
                        <table>
                            <thead>
                                <tr>
                                    {% for key in sql_result.data[0].keys() %}
                                    <th>{{ key }}</th>
                                    {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for row in sql_result.data %}
                                <tr>
                                    {% for value in row.values() %}
                                    <td>{{ value }}</td>
                                    {% endfor %}
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                        {% endif %}
                        
                        {% if sql_result.extracted_variables %}
                        <h5>提取的变量</h5>
                        <table>
                            <thead>
                                <tr>
                                    <th>变量名</th>
                                    <th>值</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for key, value in sql_result.extracted_variables.items() %}
                                <tr>
                                    <td>{{ key }}</td>
                                    <td>{{ value }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
                
                {% if step.variables %}
                <div class="step-section">
                    <div class="step-section-title">提取的变量</div>
                    <table>
                        <thead>
                            <tr>
                                <th>变量名</th>
                                <th>值</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for key, value in step.variables.items() %}
                            <tr>
                                <td>{{ key }}</td>
                                <td>{{ value }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>

    <div class="footer">
        <p>生成时间: {{ current_time }} | API自动化测试报告</p>
    </div>

    <script>
        function toggleStepContent(stepId) {
            var content = document.getElementById(stepId);
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        }
    </script>
</body>
</html>
"""
        
        # 写入模板文件
        template_path = os.path.join(self.template_dir, 'report_template.html')
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_content)


# 创建报告生成器单例
report_generator = ReportGenerator()