#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试报告服务层
"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import select, delete, func
from backend.database.db import async_db_session
from backend.plugin.api_testing.model.models import ApiTestReport
from backend.plugin.api_testing.schema.request import TestReportCreateRequest


class TestReportService:
    """API测试报告服务类"""

    @staticmethod
    async def create_test_report(report_data: TestReportCreateRequest) -> ApiTestReport:
        """创建测试报告"""
        async with async_db_session() as db:
            test_report = ApiTestReport(
                test_case_id=report_data.test_case_id,
                name=report_data.name,
                success=report_data.success,
                total_steps=report_data.total_steps,
                success_steps=report_data.success_steps,
                fail_steps=report_data.fail_steps,
                start_time=report_data.start_time,
                end_time=report_data.end_time,
                duration=report_data.duration,
                details=report_data.details
            )
            db.add(test_report)
            await db.commit()
            await db.refresh(test_report)
            return test_report

    @staticmethod
    async def get_test_report_by_id(report_id: int) -> Optional[ApiTestReport]:
        """根据ID获取测试报告"""
        async with async_db_session() as db:
            result = await db.execute(select(ApiTestReport).where(ApiTestReport.id == report_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def get_test_reports(
            test_case_id: Optional[int] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            success_only: Optional[bool] = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[ApiTestReport]:
        """获取测试报告列表"""
        async with async_db_session() as db:
            query = select(ApiTestReport).order_by(ApiTestReport.create_time.desc())

            if test_case_id:
                query = query.where(ApiTestReport.test_case_id == test_case_id)

            if start_date:
                query = query.where(ApiTestReport.create_time >= start_date)

            if end_date:
                query = query.where(ApiTestReport.create_time <= end_date)

            if success_only is not None:
                query = query.where(ApiTestReport.success == success_only)

            query = query.offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()

    @staticmethod
    async def delete_test_report(report_id: int) -> bool:
        """删除测试报告"""
        async with async_db_session() as db:
            result = await db.execute(delete(ApiTestReport).where(ApiTestReport.id == report_id))
            await db.commit()
            return result.rowcount > 0

    @staticmethod
    async def get_test_report_count(
            test_case_id: Optional[int] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            success_only: Optional[bool] = None
    ) -> int:
        """获取测试报告总数"""
        async with async_db_session() as db:
            query = select(func.count(ApiTestReport.id))

            if test_case_id:
                query = query.where(ApiTestReport.test_case_id == test_case_id)

            if start_date:
                query = query.where(ApiTestReport.create_time >= start_date)

            if end_date:
                query = query.where(ApiTestReport.create_time <= end_date)

            if success_only is not None:
                query = query.where(ApiTestReport.success == success_only)

            result = await db.execute(query)
            return result.scalar()

    @staticmethod
    async def get_report_statistics(
            test_case_id: Optional[int] = None,
            days: int = 30
    ) -> dict:
        """获取测试报告统计信息"""
        async with async_db_session() as db:
            # 计算时间范围
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # 基础查询
            base_query = select(ApiTestReport).where(
                ApiTestReport.create_time >= start_date,
                ApiTestReport.create_time <= end_date
            )

            if test_case_id:
                base_query = base_query.where(ApiTestReport.test_case_id == test_case_id)

            # 总数统计
            total_result = await db.execute(select(func.count(ApiTestReport.id)).select_from(base_query.subquery()))
            total_count = total_result.scalar()

            # 成功数统计
            success_result = await db.execute(
                select(func.count(ApiTestReport.id))
                    .select_from(base_query.where(ApiTestReport.success == True).subquery())
            )
            success_count = success_result.scalar()

            # 失败数统计
            fail_count = total_count - success_count

            # 成功率计算
            success_rate = (success_count / total_count * 100) if total_count > 0 else 0

            # 平均执行时间
            avg_duration_result = await db.execute(
                select(func.avg(ApiTestReport.duration))
                    .select_from(base_query.subquery())
            )
            avg_duration = avg_duration_result.scalar() or 0

            return {
                "total_count": total_count,
                "success_count": success_count,
                "fail_count": fail_count,
                "success_rate": round(success_rate, 2),
                "avg_duration": round(avg_duration, 2),
                "period_days": days,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }

    @staticmethod
    async def cleanup_old_reports(days: int = 90) -> int:
        """清理旧的测试报告"""
        async with async_db_session() as db:
            cutoff_date = datetime.now() - timedelta(days=days)
            result = await db.execute(
                delete(ApiTestReport).where(ApiTestReport.create_time < cutoff_date)
            )
            await db.commit()
            return result.rowcount
