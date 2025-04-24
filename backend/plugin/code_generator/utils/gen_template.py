#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pydantic.alias_generators import to_pascal, to_snake

from backend.core.conf import settings
from backend.plugin.code_generator.model import GenBusiness, GenColumn
from backend.plugin.code_generator.path_conf import JINJA2_TEMPLATE_DIR


class GenTemplate:
    def __init__(self) -> None:
        """初始化模板生成器"""
        self.env = Environment(
            loader=FileSystemLoader(JINJA2_TEMPLATE_DIR),
            autoescape=select_autoescape(enabled_extensions=['jinja']),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            enable_async=True,
        )
        self.init_content = '#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n'

    def get_template(self, jinja_file: str) -> Template:
        """
        获取模板文件

        :param jinja_file: Jinja2 模板文件
        :return:
        """
        return self.env.get_template(jinja_file)

    @staticmethod
    def get_template_files() -> list[str]:
        """
        获取模板文件列表

        :return:
        """
        files = []

        # python
        python_template_path = JINJA2_TEMPLATE_DIR / 'python'
        files.extend([f'python/{file.name}' for file in python_template_path.iterdir() if file.is_file()])

        return files

    @staticmethod
    def get_code_gen_paths(business: GenBusiness) -> list[str]:
        """
        获取代码生成路径列表

        :param business: 代码生成业务对象
        :return:
        """
        app_name = business.app_name
        filename = business.filename
        return [
            f'{app_name}/api/{business.api_version}/{filename}.py',
            f'{app_name}/crud/crud_{filename}.py',
            f'{app_name}/model/{filename}.py',
            f'{app_name}/schema/{filename}.py',
            f'{app_name}/service/{filename}_service.py',
        ]

    def get_code_gen_path(self, tpl_path: str, business: GenBusiness) -> str:
        """
        获取代码生成路径

        :param tpl_path: 模板文件路径
        :param business: 代码生成业务对象
        :return:
        """
        target_files = self.get_code_gen_paths(business)
        code_gen_path_mapping = dict(zip(self.get_template_files(), target_files))
        return code_gen_path_mapping[tpl_path]

    @staticmethod
    def get_vars(business: GenBusiness, models: Sequence[GenColumn]) -> dict[str, str | Sequence[GenColumn]]:
        """
        获取模板变量

        :param business: 代码生成业务对象
        :param models: 代码生成模型对象列表
        :return:
        """
        return {
            'app_name': business.app_name,
            'table_name': to_snake(business.table_name),
            'doc_comment': business.doc_comment,
            'table_comment': business.table_comment,
            'class_name': to_pascal(business.class_name),
            'instance_name': to_snake(business.class_name),
            'schema_name': to_pascal(business.schema_name),
            'default_datetime_column': business.default_datetime_column,
            'permission': str(business.table_name.replace('_', ':')),
            'database_type': settings.DATABASE_TYPE,
            'models': models,
        }


gen_template: GenTemplate = GenTemplate()
