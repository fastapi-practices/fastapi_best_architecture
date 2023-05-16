#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import pytest
from httpx import AsyncClient

sys.path.append('../../')

from backend.app.common.redis import redis_client  # noqa: E402
from backend.app.core.conf import settings  # noqa: E402


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='package', autouse=True)
async def function_fixture(anyio_backend):
    auth_data = {
        'url': f'http://{settings.UVICORN_HOST}:{settings.UVICORN_PORT}/v1/auth/users/login',
        'headers': {'accept': 'application/json', 'Content-Type': 'application/json'},
        'json': {'username': 'test', 'password': 'test'},
    }
    async with AsyncClient() as client:
        response = await client.post(**auth_data)
        token = response.json()['data']['access_token']
        test_token = await redis_client.get('test_token')
        if not test_token:
            await redis_client.set('test_token', token, ex=86400)
