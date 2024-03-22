#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.task.celery import celery_app


@celery_app.task(name='auto_delete_db_log')
def auto_delete_db_log() -> int:
    # TODO
    ...
