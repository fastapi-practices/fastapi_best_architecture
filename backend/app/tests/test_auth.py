#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import pytest
from httpx import AsyncClient

sys.path.append('../../')

from backend.app.core.conf import settings  # noqa: E402
from backend.app.main import app  # noqa: E402


class TestUser:
    pytestmark = pytest.mark.anyio

    async def test_login(self):
        async with AsyncClient(
            app=app, headers={'accept': 'application/json', 'Content-Type': 'application/json'}
        ) as client:
            response = await client.post(
                url=f'http://{settings.UVICORN_HOST}:{settings.UVICORN_PORT}/v1/auth/users/login',
                json={'username': 'test', 'password': 'test'},
            )
        assert response.status_code == 200
        assert response.json()['data']['token_type'] == 'Bearer'
