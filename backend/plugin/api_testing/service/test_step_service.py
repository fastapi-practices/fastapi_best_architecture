#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试步骤服务层
"""
from typing import List, Optional
from sqlalchemy import select, update, delete
from backend.database.db import async_db_session
from backend.plugin.api_testing.model.models import ApiTestStep
from backend.plugin.api_testing.schema.request import TestStepCreateRequest, TestStepUpdateRequest


class TestStepService:
    """API测试步骤服务类"""

    @staticmethod
    async def create_test_step(step_data: TestStepCreateRequest) -> ApiTestStep:
        """创建测试步骤"""
        async with async_db_session() as db:
            test_step = ApiTestStep(
                name=step_data.name,
                test_case_id=step_data.test_case_id,
                url=step_data.url,
                method=step_data.method,
                headers=step_data.headers,
                params=step_data.params,
                body=step_data.body,
                files=step_data.files,
                auth=step_data.auth,
                extract=step_data.extract,
                validate=step_data.validate,
                sql_queries=step_data.sql_queries,
                timeout=step_data.timeout,
                retry=step_data.retry,
                retry_interval=step_data.retry_interval,
                order=step_data.order,
                status=step_data.status
            )
            db.add(test_step)
            await db.commit()
            await db.refresh(test_step)
            return test_step

    @staticmethod
    async def get_test_step_by_id(step_id: int) -> Optional[ApiTestStep]:
        """根据ID获取测试步骤"""
        async with async_db_session() as db:
            result = await db.execute(select(ApiTestStep).where(ApiTestStep.id == step_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def get_test_steps(test_case_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[ApiTestStep]:
        """获取测试步骤列表"""
        async with async_db_session() as db:
            query = select(ApiTestStep).order_by(ApiTestStep.order)

            if test_case_id:
                query = query.where(ApiTestStep.test_case_id == test_case_id)

            query = query.offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()

    @staticmethod
    async def update_test_step(step_id: int, step_data: TestStepUpdateRequest) -> Optional[ApiTestStep]:
        """更新测试步骤"""
        async with async_db_session() as db:
            # 构建更新数据
            update_data = {}
            if step_data.name is not None:
                update_data['name'] = step_data.name
            if step_data.url is not None:
                update_data['url'] = step_data.url
            if step_data.method is not None:
                update_data['method'] = step_data.method
            if step_data.headers is not None:
                update_data['headers'] = step_data.headers
            if step_data.params is not None:
                update_data['params'] = step_data.params
            if step_data.body is not None:
                update_data['body'] = step_data.body
            if step_data.files is not None:
                update_data['files'] = step_data.files
            if step_data.auth is not None:
                update_data['auth'] = step_data.auth
            if step_data.extract is not None:
                update_data['extract'] = step_data.extract
            if step_data.validate is not None:
                update_data['validate'] = step_data.validate
            if step_data.sql_queries is not None:
                update_data['sql_queries'] = step_data.sql_queries
            if step_data.timeout is not None:
                update_data['timeout'] = step_data.timeout
            if step_data.retry is not None:
                update_data['retry'] = step_data.retry
            if step_data.retry_interval is not None:
                update_data['retry_interval'] = step_data.retry_interval
            if step_data.order is not None:
                update_data['order'] = step_data.order
            if step_data.status is not None:
                update_data['status'] = step_data.status

            if update_data:
                await db.execute(
                    update(ApiTestStep)
                        .where(ApiTestStep.id == step_id)
                        .values(**update_data)
                )
                await db.commit()

            # 返回更新后的步骤
            result = await db.execute(select(ApiTestStep).where(ApiTestStep.id == step_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def delete_test_step(step_id: int) -> bool:
        """删除测试步骤"""
        async with async_db_session() as db:
            result = await db.execute(delete(ApiTestStep).where(ApiTestStep.id == step_id))
            await db.commit()
            return result.rowcount > 0

    @staticmethod
    async def get_test_step_count(test_case_id: Optional[int] = None) -> int:
        """获取测试步骤总数"""
        async with async_db_session() as db:
            query = select(ApiTestStep)
            if test_case_id:
                query = query.where(ApiTestStep.test_case_id == test_case_id)
            result = await db.execute(query)
            return len(result.scalars().all())

    @staticmethod
    async def reorder_steps(test_case_id: int, step_orders: List[dict]) -> bool:
        """重新排序测试步骤"""
        async with async_db_session() as db:
            try:
                for item in step_orders:
                    await db.execute(
                        update(ApiTestStep)
                            .where(ApiTestStep.id == item['step_id'])
                            .where(ApiTestStep.test_case_id == test_case_id)
                            .values(order=item['order'])
                    )
                await db.commit()
                return True
            except Exception:
                await db.rollback()
                return False
