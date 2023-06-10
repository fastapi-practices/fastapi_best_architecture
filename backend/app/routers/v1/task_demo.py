#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1 import task_demo as task_demo_views

router = APIRouter()

router.add_api_route(
    path='',
    endpoint=task_demo_views.get_all_task_demos,
    methods=['GET'],
    summary='获取所有任务示例',
)

router.add_api_route(
    path='',
    endpoint=task_demo_views.create_sync_task_demo,
    methods=['POST'],
    summary='创建同步任务示例',
)

router.add_api_route(
    path='/async',
    endpoint=task_demo_views.create_async_task_demo,
    methods=['POST'],
    summary='创建异步任务示例',
)

router.add_api_route(
    path='',
    endpoint=task_demo_views.delete_task_demo,
    methods=['DELETE'],
    summary='删除任务示例',
)
