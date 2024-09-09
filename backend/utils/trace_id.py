#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Request

from backend.core.conf import settings


def get_request_trace_id(request: Request) -> str:
    return request.headers.get(settings.TRACE_ID_REQUEST_HEADER_KEY) or '-'
