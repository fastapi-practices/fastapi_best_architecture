#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试用例服务层
"""
from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from backend.database.db import async_db_session
from backend.plugin.api_testing.model.models import ApiTestCase
from backend.plugin.api_testing.schema.request import TestCaseCreateRequest, TestCaseUpdateRequest


class TestCaseService:
    """API测试用例服务类"""

    @staticmethod
    async def create_test_case(case_data: TestCaseCreateRequest) -> ApiTestCase:
        """创建测试用例"""
        async with async_db_session() as db:
            test_case = ApiTestCase(
                name=case_data.name,
                project_id=case_data.project_id,
                description=case_data.description,
                pre_script=case_data.pre_script,
                post_script=case_data.post_script,
                status=case_data.status
            )
            db.add(test_case)
            await db.commit()
            await db.refresh(test_case)
            return test_case

    @staticmethod
    async def get_test_case_by_id(case_id: int) -> Optional[ApiTestCase]:
        """根据ID获取测试用例"""
        async with async_db_session() as db:
            result = await db.execute(
                select(ApiTestCase)
                .options(selectinload(ApiTestCase.steps))
                .where(ApiTestCase.id == case_id)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def get_test_cases(project_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[ApiTestCase]:
        """获取测试用例列表"""
        async with async_db_session() as db:
            query = select(ApiTestCase).options(selectinload(ApiTestCase.steps))

            if project_id:
                query = query.where(ApiTestCase.project_id == project_id)

            query = query.offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()

    @staticmethod
    async def update_test_case(case_id: int, case_data: TestCaseUpdateRequest) -> Optional[ApiTestCase]:
        """更新测试用例"""
        async with async_db_session() as db:
            # 构建更新数据
            update_data = {}
            if case_data.name is not None:
                update_data['name'] = case_data.name
            if case_data.description is not None:
                update_data['description'] = case_data.description
            if case_data.pre_script is not None:
                update_data['pre_script'] = case_data.pre_script
            if case_data.post_script is not None:
                update_data['post_script'] = case_data.post_script
            if case_data.status is not None:
                update_data['status'] = case_data.status

            if update_data:
                await db.execute(
                    update(ApiTestCase)
                    .where(ApiTestCase.id == case_id)
                    .values(**update_data)
                )
                await db.commit()

            # 返回更新后的用例
            result = await db.execute(
                select(ApiTestCase)
                .options(selectinload(ApiTestCase.steps))
                .where(ApiTestCase.id == case_id)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def delete_test_case(case_id: int) -> bool:
        """删除测试用例"""
        async with async_db_session() as db:
            result = await db.execute(delete(ApiTestCase).where(ApiTestCase.id == case_id))
            await db.commit()
            return result.rowcount > 0

    @staticmethod
    async def get_test_case_count(project_id: Optional[int] = None) -> int:
        """获取测试用例总数"""
        async with async_db_session() as db:
            query = select(ApiTestCase)
            if project_id:
                query = query.where(ApiTestCase.project_id == project_id)
            result = await db.execute(query)
            return len(result.scalars().all())
