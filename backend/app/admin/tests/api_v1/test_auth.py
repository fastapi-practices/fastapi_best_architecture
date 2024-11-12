#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from starlette.testclient import TestClient


def test_logout(client: TestClient, token_headers: dict[str, str]) -> None:
    response = client.post('/auth/logout', headers=token_headers)
    assert response.status_code == 200
    assert response.json()['code'] == 200
