#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('../../')

from typing import Dict, Generator

import pytest

from starlette.testclient import TestClient

from backend.app.database.db_mysql import get_db
from backend.app.main import app
from backend.app.tests.utils.db_mysql import override_get_db
from backend.app.tests.utils.get_headers import get_token_headers

app.dependency_overrides[get_db] = override_get_db


# Test user
PYTEST_USERNAME = 'admin'
PYTEST_PASSWORD = '123456'


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='module')
def token_headers(client: TestClient) -> Dict[str, str]:
    return get_token_headers(client=client, username=PYTEST_USERNAME, password=PYTEST_PASSWORD)
