#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import zipfile

from backend.app.generator.crud.crud_gen_business import gen_business_dao
from backend.app.generator.model import GenBusiness
from backend.app.generator.service.gen_business_service import gen_business_service
from backend.app.generator.service.gen_model_service import gen_model_service
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session
from backend.utils.gen_template import gen_template
from backend.utils.serializers import select_as_dict, select_list_serialize


class GenService:
    @staticmethod
    async def get_business_and_model(*, pk: int) -> dict:
        gen_business = await gen_business_service.get(pk=pk)
        gen_models = await gen_model_service.get_by_business(business_id=pk)
        business_data = await select_as_dict(gen_business)
        if gen_models:
            model_data = await select_list_serialize(gen_models)
            business_data.update({'models': model_data})
        return business_data

    @staticmethod
    async def render_tpl_code(*, business: GenBusiness) -> dict:
        gen_models = await gen_model_service.get_by_business(business_id=business.id)
        if not gen_models:
            raise errors.NotFoundError(msg='代码生成模型表为空')
        gen_vars = gen_template.get_vars(business, gen_models)
        tpl_code_map = {}
        for tpl_path in gen_template.get_template_paths():
            tpl_code_map[tpl_path] = await gen_template.get_template(tpl_path).render_async(**gen_vars)
        return tpl_code_map

    async def preview(self, *, pk: int) -> dict:
        async with async_db_session() as db:
            business = await gen_business_dao.get(db, pk)
            if not business:
                raise errors.NotFoundError(msg='业务不存在')
            tpl_code_map = await self.render_tpl_code(business=business)
            return {
                tpl.replace('.jinja', '.py') if tpl.startswith('py') else ...: code
                for tpl, code in tpl_code_map.items()
            }

    @staticmethod
    async def generate() -> dict: ...

    async def download(self, *, pk: int) -> io.BytesIO:
        async with async_db_session() as db:
            business = await gen_business_dao.get(db, pk)
            if not business:
                raise errors.NotFoundError(msg='业务不存在')
        bio = io.BytesIO()
        zf = zipfile.ZipFile(bio, 'w')
        app_name = business.app_name
        tpl_code_map = await self.render_tpl_code(business=business)
        for code_path, code in tpl_code_map.items():
            new_code_path = gen_template.get_code_gen_path(code_path, app_name)
            zf.writestr(new_code_path, code)
        zf.close()
        bio.seek(0)
        return bio


gen_service = GenService()
