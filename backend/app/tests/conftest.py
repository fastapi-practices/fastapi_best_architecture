#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('../../')

import pytest
from typing import Generator, Dict

from starlette.testclient import TestClient

from backend.app.main import app
from backend.app.core.conf import settings
from backend.app.tests.utils.get_headers import get_token_headers


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='module')
def token_headers(client: TestClient) -> Dict[str, str]:
    return get_token_headers(client=client, username=settings.TEST_USERNAME, password=settings.TEST_USER_PASSWORD)
