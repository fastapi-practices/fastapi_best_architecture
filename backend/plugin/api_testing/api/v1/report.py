#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试报告API
"""
from typing import Any, Dict
from fastapi import APIRouter, Body
from fastapi.responses import HTMLResponse
from backend.common.response.response_schema import response_base, ResponseModel, ResponseSchemaModel
from backend.plugin.api_testing.utils.report_generator import ReportFormat, TestReport, report_generator

router = APIRouter()


@router.post("/generate", response_model=Dict[str, Any], summary="生成测试报告")
async def generate_report(
        report_data: TestReport = Body(...),
        format: ReportFormat = Body(ReportFormat.HTML)
) -> ResponseModel | ResponseSchemaModel:
    """
    生成测试报告接口
    
    根据提供的测试数据生成HTML或JSON格式的测试报告
    """
    try:
        # 生成报告
        report_content = report_generator.generate_report(report_data, format)

        # 构建响应
        data = {"content": report_content, "format": format}

        return response_base.success(data=data)
    except Exception as e:
        return response_base.fail(data=f"报告生成失败: {str(e)}")


@router.post("/preview", response_class=HTMLResponse, summary="预览HTML测试报告")
async def preview_html_report(
        report_data: TestReport = Body(...)
) -> HTMLResponse:
    """
    预览HTML测试报告
    
    根据提供的测试数据生成并直接返回HTML格式的测试报告用于预览
    """
    try:
        # 生成HTML报告
        report_content = report_generator.generate_report(report_data, ReportFormat.HTML)

        # 直接返回HTML内容
        return HTMLResponse(content=report_content)
    except Exception as e:
        error_html = f"""
        <html>
            <body>
                <h1>报告生成失败</h1>
                <p>错误信息: {str(e)}</p>
            </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=500)
