#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GenBusinessService:
    @staticmethod
    async def create() -> None: ...

    @staticmethod
    async def update() -> int: ...

    @staticmethod
    async def delete() -> int: ...


gen_business_service = GenBusinessService()
