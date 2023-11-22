#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from starlette.testclient import TestClient

from backend.app.core.conf import settings
from backend.app.tests.conftest import PYTEST_PASSWORD, PYTEST_USERNAME


def test_login(client: TestClient) -> None:
    data = {
        'username': PYTEST_USERNAME,
        'password': PYTEST_PASSWORD,
    }
    response = client.post(f'{settings.API_V1_STR}/auth/swagger_login', data=data)
    assert response.status_code == 200
    assert response.json()['token_type'] == 'Bearer'


def test_logout(client: TestClient, token_headers: dict[str, str]) -> None:
    response = client.post(f'{settings.API_V1_STR}/auth/logout', headers=token_headers)
    assert response.status_code == 200
    assert response.json()['code'] == 200
