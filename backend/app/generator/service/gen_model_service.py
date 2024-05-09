#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GenModelService:
    @staticmethod
    async def create() -> None: ...

    @staticmethod
    async def update() -> int: ...

    @staticmethod
    async def delete() -> int: ...


gen_model_service = GenModelService()
