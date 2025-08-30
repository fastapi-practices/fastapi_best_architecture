#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API项目服务层
"""
from typing import List, Optional
from sqlalchemy import select, update, delete
from backend.database.db import async_db_session
from backend.plugin.api_testing.model.models import ApiProject
from backend.plugin.api_testing.schema.request import ProjectCreateRequest, ProjectUpdateRequest


class ProjectService:
    """API项目服务类"""

    @staticmethod
    async def create_project(project_data: ProjectCreateRequest) -> ApiProject:
        """创建API项目"""
        async with async_db_session() as db:
            project = ApiProject(
                name=project_data.name,
                description=project_data.description,
                base_url=project_data.base_url,
                headers=project_data.headers,
                variables=project_data.variables,
                status=project_data.status
            )
            db.add(project)
            await db.commit()
            await db.refresh(project)
            return project

    @staticmethod
    async def get_project_by_id(project_id: int) -> Optional[ApiProject]:
        """根据ID获取API项目"""
        async with async_db_session() as db:
            result = await db.execute(select(ApiProject).where(ApiProject.id == project_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def get_projects(skip: int = 0, limit: int = 100) -> List[ApiProject]:
        """获取API项目列表"""
        async with async_db_session() as db:
            result = await db.execute(select(ApiProject).offset(skip).limit(limit))
            return result.scalars().all()

    @staticmethod
    async def update_project(project_id: int, project_data: ProjectUpdateRequest) -> Optional[ApiProject]:
        """更新API项目"""
        async with async_db_session() as db:
            # 构建更新数据
            update_data = {}
            if project_data.name is not None:
                update_data['name'] = project_data.name
            if project_data.description is not None:
                update_data['description'] = project_data.description
            if project_data.base_url is not None:
                update_data['base_url'] = project_data.base_url
            if project_data.headers is not None:
                update_data['headers'] = project_data.headers
            if project_data.variables is not None:
                update_data['variables'] = project_data.variables
            if project_data.status is not None:
                update_data['status'] = project_data.status

            if update_data:
                await db.execute(
                    update(ApiProject)
                    .where(ApiProject.id == project_id)
                    .values(**update_data)
                )
                await db.commit()

            # 返回更新后的项目
            result = await db.execute(select(ApiProject).where(ApiProject.id == project_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def delete_project(project_id: int) -> bool:
        """删除API项目"""
        async with async_db_session() as db:
            result = await db.execute(delete(ApiProject).where(ApiProject.id == project_id))
            await db.commit()
            return result.rowcount > 0

    @staticmethod
    async def get_project_count() -> int:
        """获取项目总数"""
        async with async_db_session() as db:
            result = await db.execute(select(ApiProject))
            return len(result.scalars().all())
