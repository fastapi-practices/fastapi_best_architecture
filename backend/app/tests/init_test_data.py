#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('../../')

import asyncio

from backend.app.init_test_data import InitTestData
from backend.app.tests.utils.db_mysql import async_db_session, create_table

if __name__ == '__main__':
    init = InitTestData(session=async_db_session)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_table())
    loop.run_until_complete(init.init_data())
