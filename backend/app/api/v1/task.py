#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.common.rbac import DependsRBAC
from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.response.response_schema import response_base
from backend.app.services.task_service import TaskService

router = APIRouter()


@router.get('', summary='获取任务列表', dependencies=[DependsJwtAuth])
async def get_all_tasks():
    tasks_list = await TaskService.get_task_list()
    return await response_base.success(data=tasks_list)


@router.get('/{pk}', summary='获取任务详情', dependencies=[DependsJwtAuth])
async def get_task(pk: str):
    task = await TaskService.get_task(pk=pk)
    return await response_base.success(data=task)


@router.post('/{pk}/run', summary='执行任务', dependencies=[DependsRBAC])
async def run_task(pk: str):
    task = await TaskService().run(pk=pk)
    return await response_base.success(data=task)


@router.post('/{pk}/pause', summary='暂停任务', dependencies=[DependsRBAC])
async def pause_task(pk: str):
    task = await TaskService().pause(pk=pk)
    return await response_base.success(data=task)


@router.post('/{pk}/resume', summary='恢复任务', dependencies=[DependsRBAC])
async def resume_task(pk: str):
    task = await TaskService().resume(pk=pk)
    return await response_base.success(data=task)


@router.post('/{pk}/stop', summary='删除任务', dependencies=[DependsRBAC])
async def delete_task(pk: str):
    task = await TaskService().delete(pk=pk)
    return await response_base.success(data=task)
