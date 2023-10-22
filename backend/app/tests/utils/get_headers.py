#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Dict

from starlette.testclient import TestClient

from backend.app.core.conf import settings


def get_token_headers(client: TestClient, username: str, password: str) -> Dict[str, str]:
    data = {
        'username': username,
        'password': password,
    }
    response = client.post(f'{settings.API_V1_STR}/auth/swagger_login', data=data)
    token_type = response.json()['token_type']
    access_token = response.json()['access_token']
    headers = {'Authorization': f'{token_type} {access_token}'}
    return headers
