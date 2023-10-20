#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery.exceptions import BackendGetMetaError
from celery.result import AsyncResult
from fastapi import APIRouter, Path

from backend.app.common.exception.errors import NotFoundError
from backend.app.common.response.response_code import CustomResponseCode
from backend.app.common.response.response_schema import response_base

router = APIRouter()


@router.get('/{pk}', summary='获取任务结果')
async def get_task_result(pk: str = Path(description='任务ID')):
    try:
        task = AsyncResult(pk)
    except BackendGetMetaError:
        raise NotFoundError(msg='任务不存在')
    else:
        status = task.status
        if status == 'FAILURE':
            return await response_base.fail(res=CustomResponseCode.HTTP_204, data=task.result)
        return await response_base.success(data=task.result)
