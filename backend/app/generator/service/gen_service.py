#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import os.path
import zipfile

from pathlib import Path
from typing import Sequence

import aiofiles

from backend.app.generator.crud.crud_gen import gen_dao
from backend.app.generator.crud.crud_gen_business import gen_business_dao
from backend.app.generator.crud.crud_gen_model import gen_model_dao
from backend.app.generator.model import GenBusiness
from backend.app.generator.schema.gen_business import CreateGenBusinessParam
from backend.app.generator.schema.gen_model import CreateGenModelParam
from backend.app.generator.service.gen_business_service import gen_business_service
from backend.app.generator.service.gen_model_service import gen_model_service
from backend.common.enums import GenModelType
from backend.common.exception import errors
from backend.core.path_conf import BasePath
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
    async def get_tables(*, table_schema: str) -> Sequence[str]:
        async with async_db_session() as db:
            return await gen_dao.get_all_tables(db, table_schema)

    @staticmethod
    async def import_business_and_model(*, app: str, table_schema: str, table_name: str) -> None:
        async with async_db_session.begin() as db:
            table_info = await gen_dao.get_table(db, table_name)
            if not table_info:
                raise errors.NotFoundError(msg='数据库表不存在')
            table_name = table_info[0]
            business_data = {
                'app_name': app,
                'table_name_en': table_name,
                'table_name_zh': table_info[1] or ' '.join(table_name.split('_')),
                'table_simple_name_zh': table_info[1] or table_name.split('_')[-1],
                'table_comment': table_info[1],
            }
            new_business = GenBusiness(**CreateGenBusinessParam(**business_data).model_dump())
            db.add(new_business)
            await db.flush()
            column_info = await gen_dao.get_all_columns(db, table_schema, table_name)
            for column in column_info:
                column_type = column[-1].split('(')[0].lower()
                model_data = {
                    'name': column[0],
                    'comment': column[-2],
                    'type': column_type,
                    'sort': column[-3],
                    'length': column[-1].split('(')[1][:-1]
                    if column_type == GenModelType.CHAR or column_type == GenModelType.VARCHAR
                    else 0,
                    'is_pk': column[1],
                    'is_nullable': column[2],
                    'gen_business_id': new_business.id,
                }
                await gen_model_dao.create(db, CreateGenModelParam(**model_data))

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
                tpl.replace('.jinja', '.py') if tpl.startswith('py') else ...: code.encode('utf-8')
                for tpl, code in tpl_code_map.items()
            }

    async def generate(self, *, pk: int) -> None:
        async with async_db_session() as db:
            business = await gen_business_dao.get(db, pk)
            if not business:
                raise errors.NotFoundError(msg='业务不存在')
            tpl_code_map = await self.render_tpl_code(business=business)
            gen_path = business.gen_path
            if not gen_path:
                gen_path = os.path.join(BasePath, 'app')
            for tpl_path, code in tpl_code_map.items():
                code_filepath = os.path.join(
                    gen_path,
                    *gen_template.get_code_gen_path(tpl_path, business).split('/')[1:],
                )
                code_folder = Path(str(code_filepath)).parent
                if not code_folder.exists():
                    code_folder.mkdir(parents=True, exist_ok=True)
                async with aiofiles.open(code_filepath, 'w', encoding='utf-8') as f:
                    await f.write(code)

    async def download(self, *, pk: int) -> io.BytesIO:
        async with async_db_session() as db:
            business = await gen_business_dao.get(db, pk)
            if not business:
                raise errors.NotFoundError(msg='业务不存在')
        bio = io.BytesIO()
        zf = zipfile.ZipFile(bio, 'w')
        tpl_code_map = await self.render_tpl_code(business=business)
        for tpl_path, code in tpl_code_map.items():
            new_code_path = gen_template.get_code_gen_path(tpl_path, business)
            zf.writestr(new_code_path, code)
        zf.close()
        bio.seek(0)
        return bio


gen_service = GenService()
