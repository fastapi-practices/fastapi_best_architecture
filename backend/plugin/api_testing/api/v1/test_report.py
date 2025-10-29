#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试报告管理接口
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Path, Query, HTTPException
from backend.common.response.response_schema import response_base, ResponseModel, ResponseSchemaModel
from backend.plugin.api_testing.service.test_report_service import TestReportService
from backend.plugin.api_testing.schema.request import (
    TestReportCreateRequest, TestReportResponse
)

router = APIRouter()


@router.post("/", response_model=ResponseModel, summary="创建测试报告")
async def create_test_report(report_data: TestReportCreateRequest) -> ResponseModel | ResponseSchemaModel:
    """
    创建测试报告
    """
    try:
        test_report = await TestReportService.create_test_report(report_data)
        report_response = TestReportResponse(
            id=test_report.id,
            test_case_id=test_report.test_case_id,
            name=test_report.name,
            success=test_report.success,
            total_steps=test_report.total_steps,
            success_steps=test_report.success_steps,
            fail_steps=test_report.fail_steps,
            start_time=test_report.start_time.isoformat(),
            end_time=test_report.end_time.isoformat(),
            duration=test_report.duration,
            details=test_report.details,
            created_time=test_report.created_time.isoformat() if test_report.created_time else ""
        )
        return response_base.success(data=report_response.model_dump())
    except ValueError as e:
        # 处理业务逻辑错误（如测试用例不存在）
        return response_base.fail(data=str(e))
    except Exception as e:
        # 处理其他未预期的错误
        return response_base.fail(data=f"创建测试报告失败: {str(e)}")


@router.get("/statistics", response_model=ResponseModel, summary="获取测试报告统计信息")
async def get_report_statistics(
        test_case_id: Optional[int] = Query(None, description="测试用例ID"),
        days: int = Query(30, description="统计天数")
) -> ResponseModel | ResponseSchemaModel:
    """
    获取测试报告统计信息
    """
    try:
        statistics = await TestReportService.get_report_statistics(test_case_id=test_case_id, days=days)
        return response_base.success(data=statistics)
    except Exception as e:
        return response_base.fail(data=f"获取统计信息失败: {str(e)}")


@router.get("/test_cases/available", response_model=ResponseModel, summary="获取可用的测试用例列表")
async def get_available_test_cases() -> ResponseModel | ResponseSchemaModel:
    """
    获取可用的测试用例列表（用于创建报告时选择）
    """
    try:
        test_cases = await TestReportService.get_available_test_cases()
        return response_base.success(data={
            "test_cases": test_cases,
            "total": len(test_cases)
        })
    except Exception as e:
        return response_base.fail(data=f"获取可用测试用例失败: {str(e)}")


@router.delete("/cleanup", response_model=ResponseModel, summary="清理旧的测试报告")
async def cleanup_old_reports(
        days: int = Query(90, description="保留天数，超过此天数的报告将被删除")
) -> ResponseModel | ResponseSchemaModel:
    """
    清理旧的测试报告
    """
    try:
        deleted_count = await TestReportService.cleanup_old_reports(days=days)
        return response_base.success(
            data={
                "deleted_count": deleted_count,
                "days": days
            }
        )
    except Exception as e:
        return response_base.fail(data=f"清理报告失败: {str(e)}")


@router.get("/", response_model=ResponseModel, summary="获取测试报告列表")
async def get_test_reports(
        test_case_id: Optional[int] = Query(None, description="测试用例ID"),
        start_date: Optional[str] = Query(None, description="开始日期 (YYYY-MM-DD)"),
        end_date: Optional[str] = Query(None, description="结束日期 (YYYY-MM-DD)"),
        success_only: Optional[bool] = Query(None, description="仅显示成功的报告"),
        skip: int = Query(0, description="跳过数量"),
        limit: int = Query(100, description="限制数量")
) -> ResponseModel | ResponseSchemaModel:
    """
    获取测试报告列表
    """
    try:
        # 解析日期参数
        start_datetime = None
        end_datetime = None
        if start_date:
            start_datetime = datetime.fromisoformat(start_date)
        if end_date:
            end_datetime = datetime.fromisoformat(end_date)

        test_reports = await TestReportService.get_test_reports(
            test_case_id=test_case_id,
            start_date=start_datetime,
            end_date=end_datetime,
            success_only=success_only,
            skip=skip,
            limit=limit
        )
        total = await TestReportService.get_test_report_count(
            test_case_id=test_case_id,
            start_date=start_datetime,
            end_date=end_datetime,
            success_only=success_only
        )

        report_list = []
        for test_report in test_reports:
            report_response = TestReportResponse(
                id=test_report.id,
                test_case_id=test_report.test_case_id,
                name=test_report.name,
                success=test_report.success,
                total_steps=test_report.total_steps,
                success_steps=test_report.success_steps,
                fail_steps=test_report.fail_steps,
                start_time=test_report.start_time.isoformat(),
                end_time=test_report.end_time.isoformat(),
                duration=test_report.duration,
                details=test_report.details,
                created_time=test_report.created_time.isoformat() if test_report.created_time else ""
            )
            report_list.append(report_response.model_dump())

        return response_base.success(
            data={
                "items": report_list,
                "total": total,
                "skip": skip,
                "limit": limit,
                "test_case_id": test_case_id,
                "start_date": start_date,
                "end_date": end_date,
                "success_only": success_only
            }
        )
    except Exception as e:
        return response_base.fail(data=f"获取测试报告列表失败: {str(e)}")


@router.get("/{report_id}", response_model=ResponseModel, summary="获取测试报告详情")
async def get_test_report(report_id: int = Path(..., description="报告ID")) -> ResponseModel | ResponseSchemaModel:
    """
    根据ID获取测试报告详情
    """
    try:
        test_report = await TestReportService.get_test_report_by_id(report_id)
        if not test_report:
            return response_base.fail(data="测试报告不存在")

        report_response = TestReportResponse(
            id=test_report.id,
            test_case_id=test_report.test_case_id,
            name=test_report.name,
            success=test_report.success,
            total_steps=test_report.total_steps,
            success_steps=test_report.success_steps,
            fail_steps=test_report.fail_steps,
            start_time=test_report.start_time.isoformat(),
            end_time=test_report.end_time.isoformat(),
            duration=test_report.duration,
            details=test_report.details,
            created_time=test_report.created_time.isoformat() if test_report.created_time else ""
        )
        return response_base.success(data=report_response.model_dump())
    except Exception as e:
        return response_base.fail(data=f"获取测试报告失败: {str(e)}")


@router.delete("/{report_id}", response_model=ResponseModel, summary="删除测试报告")
async def delete_test_report(report_id: int = Path(..., description="报告ID")) -> ResponseModel | ResponseSchemaModel:
    """
    删除测试报告
    """
    try:
        success = await TestReportService.delete_test_report(report_id)
        if not success:
            return response_base.fail(data="测试报告不存在或删除失败")

        return response_base.success(data="测试报告删除成功")
    except Exception as e:
        return response_base.fail(data=f"删除测试报告失败: {str(e)}")
