#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pydantic.alias_generators import to_pascal, to_snake

from backend.app.generator.model import GenBusiness, GenModel
from backend.core.path_conf import JINJA2_TEMPLATE_DIR


class GenTemplate:
    def __init__(self):
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
        获取模版文件

        :param jinja_file:
        :return:
        """

        return self.env.get_template(jinja_file)

    @staticmethod
    def get_template_paths() -> list[str]:
        """
        获取模版文件路径

        :return:
        """
        return [
            'py/api.jinja',
            'py/crud.jinja',
            'py/model.jinja',
            'py/schema.jinja',
            'py/service.jinja',
        ]

    @staticmethod
    def get_code_gen_path(tpl_path: str, business: GenBusiness) -> str:
        """
        获取代码生成路径

        :return:
        """
        app_name = business.app_name
        module_name = business.table_name_en
        code_gen_path_mapping = {
            'py/api.jinja': f'py/{app_name}/api/{business.api_version}/{module_name}.py',
            'py/crud.jinja': f'py/{app_name}/crud/crud_{module_name}.py',
            'py/model.jinja': f'py/{app_name}/model/{module_name}.py',
            'py/schema.jinja': f'py/{app_name}/schema/{module_name}.py',
            'py/service.jinja': f'py/{app_name}/service/{module_name}_service.py',
        }
        return code_gen_path_mapping.get(tpl_path)

    @staticmethod
    def get_vars(business: GenBusiness, models: list[GenModel]) -> dict:
        """
        获取模版变量

        :param business:
        :param models:
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
            'have_datetime_column': business.have_datetime_column,
            'permission_sign': str(business.__tablename__.replace('_', ':')),
            'models': models,
        }


gen_template = GenTemplate()
