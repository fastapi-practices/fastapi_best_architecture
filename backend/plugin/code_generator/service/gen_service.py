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
from backend.plugin.code_generator.crud.crud_column import gen_column_dao
from backend.plugin.code_generator.crud.crud_gen import gen_dao
from backend.plugin.code_generator.model import GenBusiness
from backend.plugin.code_generator.schema.business import CreateGenBusinessParam
from backend.plugin.code_generator.schema.column import CreateGenColumnParam
from backend.plugin.code_generator.schema.gen import ImportParam
from backend.plugin.code_generator.service.column_service import gen_column_service
from backend.plugin.code_generator.utils.format_code import format_python_code
from backend.plugin.code_generator.utils.gen_template import gen_template
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

        table_info = await gen_dao.get_table(db, obj.table_schema, obj.table_name)
        if not table_info:
            raise errors.NotFoundError(msg='数据库表不存在')

        business_info = await gen_business_dao.get_by_name(db, obj.table_name)
        if business_info:
            raise errors.ConflictError(msg='已存在相同数据库表业务')

        table_name = table_info['table_name']
        doc_comment = table_info['table_comment'] or table_name.split('_')[-1]
        new_business = GenBusiness(
            **CreateGenBusinessParam(
                app_name=obj.app,
                table_name=table_name,
                doc_comment=doc_comment,
                table_comment=table_info['table_comment'],
                class_name=to_pascal(table_name),
                schema_name=to_pascal(table_name),
                filename=table_name,
                tag=doc_comment,
            ).model_dump(),
        )
        db.add(new_business)
        await db.flush()

        column_info = await gen_dao.get_all_columns(db, obj.table_schema, table_name)
        for column in column_info:
            column_type = column['column_type'].split('(')[0].upper()
            pd_type = sql_type_to_pydantic(column_type)
            await gen_column_dao.create(
                db,
                CreateGenColumnParam(
                    name=column['column_name'],
                    comment=column['column_comment'],
                    type=column_type,
                    sort=column['sort'],
                    length=column['column_type'].split('(')[1][:-1]
                    if pd_type == 'str' and '(' in column['column_type']
                    else 0,
                    is_pk=column['is_pk'],
                    is_nullable=column['is_nullable'],
                    gen_business_id=new_business.id,
                ),
                pd_type=pd_type,
            )

    @staticmethod
    async def _render_tpl_code(*, db: AsyncSession, business: GenBusiness) -> dict[str, str]:
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
        template_mapping = gen_template.get_template_path_mapping(business)

        rendered_codes = {}
        for template_path, output_path in template_mapping.items():
            code = await gen_template.get_template(template_path).render_async(**gen_vars)
            if output_path.endswith('.py'):
                code = await format_python_code(code)
            rendered_codes[output_path] = code

        return rendered_codes

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

        codes = {}
        backend_path = 'fastapi_best_architecture/backend/app/'

        init_files = gen_template.get_init_files(business)
        for filepath, content in init_files.items():
            codes[f'{backend_path}{filepath}'] = content.encode('utf-8')

        rendered_codes = await self._render_tpl_code(db=db, business=business)
        for filepath, code in rendered_codes.items():
            codes[f'{backend_path}{filepath}'] = code.encode('utf-8')

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

        gen_path = business.gen_path or '<project_root>/backend/app'
        paths = []

        init_files = gen_template.get_init_files(business)
        paths.extend(os.path.join(gen_path, *filepath.split('/')) for filepath in init_files.keys())

        template_mapping = gen_template.get_template_path_mapping(business)
        paths.extend(os.path.join(gen_path, *filepath.split('/')) for filepath in template_mapping.values())

        return paths

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

        gen_path = business.gen_path or str(BASE_PATH / 'app')

        init_files = gen_template.get_init_files(business)
        for init_filepath, init_content in init_files.items():
            full_path = os.path.join(gen_path, *init_filepath.split('/'))
            init_folder = anyio.Path(full_path).parent
            await init_folder.mkdir(parents=True, exist_ok=True)
            async with await open_file(full_path, 'w', encoding='utf-8') as f:
                await f.write(init_content)

        rendered_codes = await self._render_tpl_code(db=db, business=business)
        for code_filepath, code in rendered_codes.items():
            full_path = os.path.join(gen_path, *code_filepath.split('/'))
            code_folder = anyio.Path(full_path).parent
            await code_folder.mkdir(parents=True, exist_ok=True)
            async with await open_file(full_path, 'w', encoding='utf-8') as f:
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
            init_files = gen_template.get_init_files(business)
            for init_filepath, init_content in init_files.items():
                zf.writestr(init_filepath, init_content)

            rendered_codes = await self._render_tpl_code(db=db, business=business)
            for code_filepath, code in rendered_codes.items():
                zf.writestr(code_filepath, code)

        bio.seek(0)
        return bio


gen_service: GenService = GenService()
