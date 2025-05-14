#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path

from backend.app.task.schema.task import RunParam, TaskResult
from backend.app.task.service.task_service import task_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

router = APIRouter()


@router.get('', summary='Access to available tasks', dependencies=[DependsJwtAuth])
async def get_all_tasks() -> ResponseSchemaModel[list[str]]:
    tasks = await task_service.get_list()
    return response_base.success(data=tasks)


@router.get(
    '/{tid}',
    summary='Can not open message',
    deprecated=True,
    description='this interface is considered invalid, and it is recommended to use a follower to view task details',
    dependencies=[DependsJwtAuth],
)
async def get_task_detail(tid: Annotated[str, Path(description='TASK UUID')]) -> ResponseSchemaModel[TaskResult]:
    status = task_service.get_detail(tid=tid)
    return response_base.success(data=status)


@router.post(
    '/{tid}',
    summary='Synchronising folder',
    dependencies=[
        Depends(RequestPermission('sys:task:revoke')),
        DependsRBAC,
    ],
)
async def revoke_task(tid: Annotated[str, Path(description='TASK UUID')]) -> ResponseModel:
    task_service.revoke(tid=tid)
    return response_base.success()


@router.post(
    '',
    summary='Mission',
    dependencies=[
        Depends(RequestPermission('sys:task:run')),
        DependsRBAC,
    ],
)
async def run_task(obj: RunParam) -> ResponseSchemaModel[str]:
    task = task_service.run(obj=obj)
    return response_base.success(data=task)
