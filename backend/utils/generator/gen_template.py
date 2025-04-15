#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pydantic.alias_generators import to_pascal, to_snake

from backend.app.generator.model import GenBusiness, GenModel
from backend.core.conf import settings
from backend.core.path_conf import JINJA2_TEMPLATE_DIR


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
        module_name = business.table_name_en
        return [
            f'{app_name}/api/{business.api_version}/{module_name}.py',
            f'{app_name}/crud/crud_{module_name}.py',
            f'{app_name}/model/{module_name}.py',
            f'{app_name}/schema/{module_name}.py',
            f'{app_name}/service/{module_name}_service.py',
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
    def get_vars(business: GenBusiness, models: Sequence[GenModel]) -> dict[str, str | Sequence[GenModel]]:
        """
        获取模板变量

        :param business: 代码生成业务对象
        :param models: 代码生成模型对象列表
        :return:
        """
        return {
            'app_name': business.app_name,
            'table_name_en': to_snake(business.table_name_en),
            'table_name_class': to_pascal(business.table_name_en),
            'table_name_zh': business.table_name_zh,
            'table_simple_name_zh': business.table_simple_name_zh,
            'table_comment': business.table_comment,
            'schema_name': to_pascal(business.schema_name),
            'default_datetime_column': business.default_datetime_column,
            'permission': str(business.table_name_en.replace('_', ':')),
            'database_type': settings.DATABASE_TYPE,
            'models': models,
        }


gen_template: GenTemplate = GenTemplate()
