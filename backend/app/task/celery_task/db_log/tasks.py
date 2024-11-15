#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.admin.service.login_log_service import login_log_service
from backend.app.admin.service.opera_log_service import opera_log_service
from backend.app.task.celery import celery_app


@celery_app.task(name='delete_db_opera_log')
async def delete_db_opera_log() -> int:
    """自动删除数据库操作日志"""
    result = await opera_log_service.delete_all()
    return result


@celery_app.task(name='delete_db_login_log')
async def delete_db_login_log() -> int:
    """自动删除数据库登录日志"""
    result = await login_log_service.delete_all()
    return result
