#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ruff: noqa: I001
from anyio import run

from backend.database.db import create_table


async def init() -> None:
    print('Creating initial data')
    await create_table()
    print('Initial data created')


if __name__ == '__main__':
    run(init)  # type: ignore
