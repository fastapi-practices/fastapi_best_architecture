#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.exc import SQLAlchemyError

from backend.app.admin.service.login_log_service import login_log_service
from backend.app.admin.service.opera_log_service import opera_log_service
from backend.app.task.celery import celery_app
from backend.app.task.conf import task_settings


@celery_app.task(
    name='auto_delete_db_opera_log',
    bind=True,
    retry_backoff=True,
    max_retries=task_settings.CELERY_TASK_MAX_RETRIES,
)
async def auto_delete_db_opera_log(self) -> int:
    """自动删除数据库操作日志"""
    try:
        result = await opera_log_service.delete_all()
    except SQLAlchemyError as exc:
        raise self.retry(exc=exc)
    return result


@celery_app.task(
    name='auto_delete_db_login_log',
    bind=True,
    retry_backoff=True,
    max_retries=task_settings.CELERY_TASK_MAX_RETRIES,
)
async def auto_delete_db_login_log(self) -> int:
    """自动删除数据库登录日志"""

    try:
        result = await login_log_service.delete_all()
    except SQLAlchemyError as exc:
        raise self.retry(exc=exc)
    return result
