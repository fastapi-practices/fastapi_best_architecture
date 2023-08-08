#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from starlette.testclient import TestClient

from backend.app.core.conf import settings


def test_login(client: TestClient) -> None:
    data = {
        'username': 'admin',
        'password': '123456',
    }
    response = client.post(f'{settings.API_V1_STR}/auth/login', json=data)
    assert response.status_code == 200
    assert response.json()['data']['access_token_type'] == 'Bearer'


def test_logout(client: TestClient, token_headers: dict[str, str]) -> None:
    response = client.post(f'{settings.API_V1_STR}/auth/logout', headers=token_headers)
    assert response.status_code == 200
    assert response.json()['code'] == 200
