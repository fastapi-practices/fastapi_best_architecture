#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path

from backend.app.task.schema.task import RunParam
from backend.app.task.service.task_service import task_service
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

router = APIRouter()


@router.get('', summary='获取所有可执行任务模块', dependencies=[DependsJwtAuth])
async def get_all_tasks() -> ResponseModel:
    tasks = task_service.get_list()
    return response_base.success(data=tasks)


@router.get('/running', summary='获取正在执行的任务', dependencies=[DependsJwtAuth])
async def get_current_task() -> ResponseModel:
    task = task_service.get()
    return response_base.success(data=task)


@router.get('/{tid}/status', summary='获取任务状态', dependencies=[DependsJwtAuth])
async def get_task_status(tid: Annotated[str, Path(description='任务ID')]) -> ResponseModel:
    status = task_service.get_status(tid)
    return response_base.success(data=status)


@router.get('/{tid}', summary='获取任务结果', dependencies=[DependsJwtAuth])
async def get_task_result(tid: Annotated[str, Path(description='任务ID')]) -> ResponseModel:
    task = task_service.get_result(tid)
    return response_base.success(data=task)


@router.post(
    '/{name}',
    summary='执行任务',
    dependencies=[
        Depends(RequestPermission('sys:task:run')),
        DependsRBAC,
    ],
)
async def run_task(obj: RunParam) -> ResponseModel:
    task = task_service.run(name=obj.name, args=obj.args, kwargs=obj.kwargs)
    return response_base.success(data=task)
