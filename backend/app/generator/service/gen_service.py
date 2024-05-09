#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GenService:
    @staticmethod
    async def get_all() -> dict: ...

    @staticmethod
    async def get() -> dict: ...

    @staticmethod
    async def preview() -> dict: ...

    @staticmethod
    async def generate() -> dict: ...

    @staticmethod
    async def download() -> dict: ...


gen_service = GenService()
