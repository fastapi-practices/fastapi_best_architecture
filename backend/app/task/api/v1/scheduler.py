#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path

from backend.app.task.service.scheduler_service import task_scheduler_service
from backend.common.pagination import DependsPagination
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

router = APIRouter()


@router.get('/all', summary='获取所有任务调度', dependencies=[DependsJwtAuth])
async def get_all_schedulers() -> ResponseModel:
    return response_base.success()


@router.get('/{pk}', summary='获取任务调度详情', dependencies=[DependsJwtAuth])
async def get_scheduler():
    return response_base.success()


@router.get(
    '',
    summary='分页获取所有任务调度',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_scheduler_paged():
    return response_base.success()


@router.post(
    '',
    summary='创建任务调度',
    dependencies=[
        Depends(RequestPermission('sys:task:add')),
        DependsRBAC,
    ],
)
async def create_scheduler():
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新任务调度',
    dependencies=[
        Depends(RequestPermission('sys:task:edit')),
        DependsRBAC,
    ],
)
async def update_scheduler(pk: Annotated[int, Path(description='任务调度 ID')]):
    return response_base.success()


@router.put(
    '/{pk}/status',
    summary='更新任务调度状态',
    dependencies=[
        Depends(RequestPermission('sys:task:edit')),
        DependsRBAC,
    ],
)
async def update_scheduler_status(pk: Annotated[int, Path(description='任务调度 ID')]):
    return response_base.success()


@router.delete(
    '/{pk}',
    summary='删除任务调度',
    dependencies=[
        Depends(RequestPermission('sys:task:del')),
        DependsRBAC,
    ],
)
async def delete_scheduler(pk: Annotated[int, Path(description='任务调度 ID')]):
    return response_base.success()


@router.post(
    '/{pk}/executions',
    summary='手动执行任务',
    dependencies=[
        Depends(RequestPermission('sys:task:exec')),
        DependsRBAC,
    ],
)
async def execute_task(pk: Annotated[int, Path(description='任务调度 ID')]) -> ResponseSchemaModel[str]:
    task = task_scheduler_service.execute(pk=pk)
    return response_base.success(data=task)


@router.delete(
    '/{task_id}/cancel',
    summary='撤销任务',
    dependencies=[
        Depends(RequestPermission('sys:task:revoke')),
        DependsRBAC,
    ],
)
async def revoke_task(task_id: Annotated[str, Path(description='任务 UUID')]) -> ResponseModel:
    task_scheduler_service.revoke(task_id=task_id)
    return response_base.success()
