#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.generator.service.gen_business_service import gen_business_service
from backend.app.generator.service.gen_model_service import gen_model_service
from backend.utils.serializers import select_as_dict, select_list_serialize


class GenService:
    @staticmethod
    async def get_business_and_model(*, pk: int) -> dict:
        gen_business = await gen_business_service.get(pk=pk)
        gen_model = await gen_model_service.get_with_relation(pk=pk)
        business_data = await select_as_dict(gen_business)
        if gen_model:
            model_data = await select_list_serialize(gen_model)
            business_data.update({'models': model_data})
        return business_data

    @staticmethod
    async def preview() -> dict: ...

    @staticmethod
    async def generate() -> dict: ...

    @staticmethod
    async def download() -> dict: ...


gen_service = GenService()
