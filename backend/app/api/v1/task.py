#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.permission import RequestPermission
from backend.app.common.rbac import DependsRBAC
from backend.app.common.response.response_code import CustomResponseCode
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.services.impl.task_service_impl import TaskService

router = APIRouter()


@router.get(
    '',
    summary='获取所有可执行任务模块',
    dependencies=[DependsJwtAuth],
)
async def get_all_tasks() -> ResponseModel:
    tasks = TaskService.get_task_list()
    return await response_base.success(data=tasks)


@router.get(
    '/{pk}',
    summary='获取任务结果',
    dependencies=[DependsJwtAuth],
)
async def get_task_result(pk: str = Path(description='任务ID')) -> ResponseModel:
    task = TaskService.get(pk)
    if not task:
        return await response_base.fail(res=CustomResponseCode.HTTP_204, data=pk)
    return await response_base.success(data=task.result)


@router.post(
    '/{module}',
    summary='执行任务',
    dependencies=[
        Depends(RequestPermission('sys:task:run')),
        DependsRBAC,
    ],
)
async def run_task(
    module: Annotated[str, Path(description='任务模块')],
    args: Annotated[list | None, Body()] = None,
    kwargs: Annotated[dict | None, Body()] = None,
) -> ResponseModel:
    task = TaskService.run(module=module, args=args, kwargs=kwargs)
    return await response_base.success(data=task.result)
