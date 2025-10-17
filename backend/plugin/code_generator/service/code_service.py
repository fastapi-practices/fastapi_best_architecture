import io
import os
import zipfile

from collections.abc import Sequence

import anyio

from anyio import open_file
from pydantic.alias_generators import to_pascal
from sqlalchemy import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.exception import errors
from backend.core.path_conf import BASE_PATH
from backend.plugin.code_generator.crud.crud_business import gen_business_dao
from backend.plugin.code_generator.crud.crud_code import gen_dao
from backend.plugin.code_generator.crud.crud_column import gen_column_dao
from backend.plugin.code_generator.model import GenBusiness
from backend.plugin.code_generator.schema.business import CreateGenBusinessParam
from backend.plugin.code_generator.schema.code import ImportParam
from backend.plugin.code_generator.schema.column import CreateGenColumnParam
from backend.plugin.code_generator.service.column_service import gen_column_service
from backend.plugin.code_generator.utils.code_template import gen_template
from backend.plugin.code_generator.utils.type_conversion import sql_type_to_pydantic


class GenService:
    """代码生成服务类"""

    @staticmethod
    async def get_tables(*, db: AsyncSession, table_schema: str) -> Sequence[RowMapping]:
        """
        获取指定 schema 下的所有表名

        :param db: 数据库会话
        :param table_schema: 数据库 schema 名称
        :return:
        """

        return await gen_dao.get_all_tables(db, table_schema)

    @staticmethod
    async def import_business_and_model(*, db: AsyncSession, obj: ImportParam) -> None:
        """
        导入业务和模型列数据

        :param db: 数据库会话
        :param obj: 导入参数对象
        :return:
        """

        table_info = await gen_dao.get_table(db, obj.table_name)
        if not table_info:
            raise errors.NotFoundError(msg='数据库表不存在')

        business_info = await gen_business_dao.get_by_name(db, obj.table_name)
        if business_info:
            raise errors.ConflictError(msg='已存在相同数据库表业务')

        table_name = table_info[0]
        new_business = GenBusiness(
            **CreateGenBusinessParam(
                app_name=obj.app,
                table_name=table_name,
                doc_comment=table_info[1] or table_name.split('_')[-1],
                table_comment=table_info[1],
                class_name=to_pascal(table_name),
                schema_name=to_pascal(table_name),
                filename=table_name,
            ).model_dump(),
        )
        db.add(new_business)
        await db.flush()

        column_info = await gen_dao.get_all_columns(db, obj.table_schema, table_name)
        for column in column_info:
            column_type = column[-1].split('(')[0].upper()
            pd_type = sql_type_to_pydantic(column_type)
            await gen_column_dao.create(
                db,
                CreateGenColumnParam(
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
    async def render_tpl_code(*, db: AsyncSession, business: GenBusiness) -> dict[str, str]:
        """
        渲染模板代码

        :param db: 数据库会话
        :param business: 业务对象
        :return:
        """
        gen_models = await gen_column_service.get_columns(db=db, business_id=business.id)
        if not gen_models:
            raise errors.NotFoundError(msg='代码生成模型表为空')

        gen_vars = gen_template.get_vars(business, gen_models)
        return {
            tpl_path: await gen_template.get_template(tpl_path).render_async(**gen_vars)
            for tpl_path in gen_template.get_template_files()
        }

    async def preview(self, *, db: AsyncSession, pk: int) -> dict[str, bytes]:
        """
        预览生成的代码

        :param db: 数据库会话
        :param pk: 业务 ID
        :return:
        """

        business = await gen_business_dao.get(db, pk)
        if not business:
            raise errors.NotFoundError(msg='业务不存在')

        tpl_code_map = await self.render_tpl_code(db=db, business=business)

        codes = {}
        for tpl_path, code in tpl_code_map.items():
            if tpl_path.startswith('python'):
                rootpath = f'fastapi_best_architecture/backend/app/{business.app_name}'
                template_name = tpl_path.split('/')[-1]
                filepath = None
                match template_name:
                    case 'api.jinja':
                        filepath = f'{rootpath}/api/{business.api_version}/{business.filename}.py'
                    case 'crud.jinja':
                        filepath = f'{rootpath}/crud/crud_{business.filename}.py'
                    case 'model.jinja':
                        filepath = f'{rootpath}/model/{business.filename}.py'
                    case 'schema.jinja':
                        filepath = f'{rootpath}/schema/{business.filename}.py'
                    case 'service.jinja':
                        filepath = f'{rootpath}/service/{business.filename}_service.py'

                if filepath:
                    codes[filepath] = code.encode('utf-8')

        return codes

    @staticmethod
    async def get_generate_path(*, db: AsyncSession, pk: int) -> list[str]:
        """
        获取代码生成路径

        :param db: 数据库会话
        :param pk: 业务 ID
        :return:
        """

        business = await gen_business_dao.get(db, pk)
        if not business:
            raise errors.NotFoundError(msg='业务不存在')

        gen_path = business.gen_path or '.../backend/app/'
        target_files = gen_template.get_code_gen_paths(business)

        return [os.path.join(gen_path, *target_file.split('/')) for target_file in target_files]

    async def generate(self, *, db: AsyncSession, pk: int) -> str:
        """
        生成代码文件

        :param db: 数据库会话
        :param pk: 业务 ID
        :return:
        """

        business = await gen_business_dao.get(db, pk)
        if not business:
            raise errors.NotFoundError(msg='业务不存在')

        tpl_code_map = await self.render_tpl_code(db=db, business=business)
        gen_path = business.gen_path or BASE_PATH / 'app'

        for tpl_path, code in tpl_code_map.items():
            code_filepath = os.path.join(
                gen_path,
                *gen_template.get_code_gen_path(tpl_path, business).split('/'),
            )

            # 写入 init 文件
            code_folder = anyio.Path(code_filepath).parent
            await code_folder.mkdir(parents=True, exist_ok=True)

            init_filepath = code_folder.joinpath('__init__.py')
            if not await init_filepath.exists():
                async with await open_file(init_filepath, 'w', encoding='utf-8') as f:
                    await f.write(gen_template.init_content)

            # api __init__.py
            if 'api' in code_filepath:
                api_init_filepath = code_folder.parent.joinpath('__init__.py')
                async with await open_file(api_init_filepath, 'w', encoding='utf-8') as f:
                    await f.write(gen_template.init_content)

            # app __init__.py
            if 'service' in code_filepath:
                app_init_filepath = code_folder.parent.joinpath('__init__.py')
                async with await open_file(app_init_filepath, 'w', encoding='utf-8') as f:
                    await f.write(gen_template.init_content)

            # model init 文件补充
            if code_folder.name == 'model':
                async with await open_file(init_filepath, 'a', encoding='utf-8') as f:
                    await f.write(
                        f'from backend.app.{business.app_name}.model.{business.table_name} '
                        f'import {to_pascal(business.table_name)}\n',
                    )

            # 写入代码文件
            async with await open_file(code_filepath, 'w', encoding='utf-8') as f:
                await f.write(code)

        return gen_path

    async def download(self, *, db: AsyncSession, pk: int) -> io.BytesIO:
        """
        下载生成的代码

        :param db: 数据库会话
        :param pk: 业务 ID
        :return:
        """

        business = await gen_business_dao.get(db, pk)
        if not business:
            raise errors.NotFoundError(msg='业务不存在')

        bio = io.BytesIO()
        with zipfile.ZipFile(bio, 'w') as zf:
            tpl_code_map = await self.render_tpl_code(db=db, business=business)
            for tpl_path, code in tpl_code_map.items():
                code_filepath = gen_template.get_code_gen_path(tpl_path, business)

                # 写入 init 文件
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

                # 写入代码文件
                zf.writestr(code_filepath, code)

        bio.seek(0)
        return bio


gen_service: GenService = GenService()
