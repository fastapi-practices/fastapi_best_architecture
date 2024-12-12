#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Generator

import pytest

from starlette.testclient import TestClient

from backend.app.admin.tests.utils.db import override_get_db
from backend.core.conf import settings
from backend.database.db import get_db
from backend.main import app

# 重载数据库
app.dependency_overrides[get_db] = override_get_db


# Test data
PYTEST_USERNAME = 'admin'
PYTEST_PASSWORD = '123456'
PYTEST_BASE_URL = f'http://testserver{settings.FASTAPI_API_V1_PATH}'


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app, base_url=PYTEST_BASE_URL) as c:
        yield c


@pytest.fixture(scope='module')
def token_headers(client: TestClient) -> dict[str, str]:
    params = {
        'username': PYTEST_USERNAME,
        'password': PYTEST_PASSWORD,
    }
    response = client.post('/auth/login/swagger', params=params)
    response.raise_for_status()
    token_type = response.json()['token_type']
    access_token = response.json()['access_token']
    headers = {'Authorization': f'{token_type} {access_token}'}
    return headers
