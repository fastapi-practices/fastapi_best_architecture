#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import os.path
import zipfile

from pathlib import Path
from typing import Sequence

import aiofiles

from pydantic.alias_generators import to_pascal

from backend.common.exception import errors
from backend.core.path_conf import BASE_PATH
from backend.database.db import async_db_session
from backend.plugin.code_generator.crud.crud_business import gen_business_dao
from backend.plugin.code_generator.crud.crud_column import gen_model_dao
from backend.plugin.code_generator.crud.crud_gen import gen_dao
from backend.plugin.code_generator.model import GenBusiness
from backend.plugin.code_generator.schema.business import CreateGenBusinessParam
from backend.plugin.code_generator.schema.column import CreateGenModelParam
from backend.plugin.code_generator.schema.gen import ImportParam
from backend.plugin.code_generator.service.column_service import gen_model_service
from backend.plugin.code_generator.utils.gen_template import gen_template
from backend.plugin.code_generator.utils.type_conversion import sql_type_to_pydantic


class GenService:
    """Code Generation Service Class"""

    @staticmethod
    async def get_tables(*, table_schema: str) -> Sequence[str]:
        """
        fetch all table names under specified schema

        :param table_schema: database schema name
        :return:
        """
        async with async_db_session() as db:
            return await gen_dao.get_all_tables(db, table_schema)

    @staticmethod
    async def import_business_and_model(*, obj: ImportParam) -> None:
        """
        Import Business and Model Data

        :param obj: import parameter object
        :return:
        """
        async with async_db_session.begin() as db:
            table_info = await gen_dao.get_table(db, obj.table_name)
            if not table_info:
                raise errors.NotFoundError(msg='Database table does not exist')

            business_info = await gen_business_dao.get_by_name(db, obj.table_name)
            if business_info:
                raise errors.ForbiddenError(msg='The same database table operation already exists')

            table_name = table_info[0]
            new_business = GenBusiness(
                **CreateGenBusinessParam(
                    app_name=obj.app,
                    table_name=table_name,
                    doc_comment=table_info[1] or table_name.split('_')[-1],
                    table_comment=table_info[1],
                    class_name=table_name,
                    schema_name=table_name,
                    filename=table_name,
                ).model_dump()
            )
            db.add(new_business)
            await db.flush()

            column_info = await gen_dao.get_all_columns(db, obj.table_schema, table_name)
            for column in column_info:
                column_type = column[-1].split('(')[0].upper()
                pd_type = sql_type_to_pydantic(column_type)
                await gen_model_dao.create(
                    db,
                    CreateGenModelParam(
                        name=column[0],
                        comment=column[-2],
                        type=column_type,
                        sort=column[-3],
                        length=column[-1].split('(')[1][:-1] if pd_type == 'str' and '(' in column[-1] else 0,
                        is_pk=column[1],
                        is_nullable=column[2],
                        gen_business_id=new_business.id,
                    ),
                    pd_type=pd_type,
                )

    @staticmethod
    async def render_tpl_code(*, business: GenBusiness) -> dict[str, str]:
        """
        Render Template Code

        :param business: business objects
        :return:
        """
        gen_models = await gen_model_service.get_by_business(business_id=business.id)
        if not gen_models:
            raise errors.NotFoundError(msg='Code Generation Model Table is empty')

        gen_vars = gen_template.get_vars(business, gen_models)
        return {
            tpl_path: await gen_template.get_template(tpl_path).render_async(**gen_vars)
            for tpl_path in gen_template.get_template_files()
        }

    async def preview(self, *, pk: int) -> dict[str, bytes]:
        """
        Preview generated code

        :param pk: Operations ID
        :return:
        """
        async with async_db_session() as db:
            business = await gen_business_dao.get(db, pk)
            if not business:
                raise errors.NotFoundError(msg='Operations do not exist')

            tpl_code_map = await self.render_tpl_code(business=business)

            codes = {}
            for tpl, code in tpl_code_map.items():
                if tpl.startswith('python'):
                    codes[tpl.replace('.jinja', '.py').split('/')[-1]] = code.encode('utf-8')

            return codes

    @staticmethod
    async def get_generate_path(*, pk: int) -> list[str]:
        """
        Get code generation path

        :param pk: Operations ID
        :return:
        """
        async with async_db_session() as db:
            business = await gen_business_dao.get(db, pk)
            if not business:
                raise errors.NotFoundError(msg='Operations do not exist')

            gen_path = business.gen_path or 'fba-backend-app-dir'
            target_files = gen_template.get_code_gen_paths(business)

            return [os.path.join(gen_path, *target_file.split('/')) for target_file in target_files]

    async def generate(self, *, pk: int) -> None:
        """
        Generate a code file

        :param pk: Operations ID
        :return:
        """
        async with async_db_session() as db:
            business = await gen_business_dao.get(db, pk)
            if not business:
                raise errors.NotFoundError(msg='Operations do not exist')

            tpl_code_map = await self.render_tpl_code(business=business)
            gen_path = business.gen_path or os.path.join(BASE_PATH, 'app')

            for tpl_path, code in tpl_code_map.items():
                code_filepath = os.path.join(
                    gen_path,
                    *gen_template.get_code_gen_path(tpl_path, business).split('/'),
                )

                # writing init files
                str_code_filepath = str(code_filepath)
                code_folder = Path(str_code_filepath).parent
                code_folder.mkdir(parents=True, exist_ok=True)

                init_filepath = code_folder.joinpath('__init__.py')
                async with aiofiles.open(init_filepath, 'w', encoding='utf-8') as f:
                    await f.write(gen_template.init_content)

                # api __init__.py
                if 'api' in str_code_filepath:
                    api_init_filepath = code_folder.parent.joinpath('__init__.py')
                    async with aiofiles.open(api_init_filepath, 'w', encoding='utf-8') as f:
                        await f.write(gen_template.init_content)

                # app __init__.py
                if 'service' in str_code_filepath:
                    app_init_filepath = code_folder.parent.joinpath('__init__.py')
                    async with aiofiles.open(app_init_filepath, 'w', encoding='utf-8') as f:
                        await f.write(gen_template.init_content)

                # model init file supplement
                if code_folder.name == 'model':
                    async with aiofiles.open(init_filepath, 'a', encoding='utf-8') as f:
                        await f.write(
                            f'from backend.app.{business.app_name}.model.{business.table_name} '
                            f'import {to_pascal(business.table_name)}\n',
                        )

                # Writing code file
                async with aiofiles.open(code_filepath, 'w', encoding='utf-8') as f:
                    await f.write(code)

    async def download(self, *, pk: int) -> io.BytesIO:
        """
        Download generated code

        :param pk: Operations ID
        :return:
        """
        async with async_db_session() as db:
            business = await gen_business_dao.get(db, pk)
            if not business:
                raise errors.NotFoundError(msg='Operations do not exist')

            bio = io.BytesIO()
            with zipfile.ZipFile(bio, 'w') as zf:
                tpl_code_map = await self.render_tpl_code(business=business)
                for tpl_path, code in tpl_code_map.items():
                    code_filepath = gen_template.get_code_gen_path(tpl_path, business)

                    # writing init files
                    code_dir = os.path.dirname(code_filepath)
                    init_filepath = os.path.join(code_dir, '__init__.py')
                    if 'model' not in code_filepath.split('/'):
                        zf.writestr(init_filepath, gen_template.init_content)
                    else:
                        zf.writestr(
                            init_filepath,
                            f'{gen_template.init_content}'
                            f'from backend.app.{business.app_name}.model.{business.table_name} '
                            f'import {to_pascal(business.table_name)}\n',
                        )

                    # api __init__.py
                    if 'api' in code_dir:
                        api_init_filepath = os.path.join(os.path.dirname(code_dir), '__init__.py')
                        zf.writestr(api_init_filepath, gen_template.init_content)

                    # app __init__.py
                    if 'service' in code_dir:
                        app_init_filepath = os.path.join(os.path.dirname(code_dir), '__init__.py')
                        zf.writestr(app_init_filepath, gen_template.init_content)

                    # Writing code file
                    zf.writestr(code_filepath, code)

            bio.seek(0)
            return bio


gen_service: GenService = GenService()
