#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ruff: noqa: I001
from anyio import run

from backend.plugin.tools import install_requirements_async


async def init() -> None:
    print('Starting initial plugin')
    await install_requirements_async()
    print('Plugin successfully installed')


if __name__ == '__main__':
    run(init)  # type: ignore
