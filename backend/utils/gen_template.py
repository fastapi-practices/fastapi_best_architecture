#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pydantic.alias_generators import to_pascal, to_snake

from backend.app.generator.conf import generator_settings
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
            f'{generator_settings.TEMPLATE_BACKEND_DIR_NAME}/api.jinja',
            f'{generator_settings.TEMPLATE_BACKEND_DIR_NAME}/crud.jinja',
            f'{generator_settings.TEMPLATE_BACKEND_DIR_NAME}/model.jinja',
            f'{generator_settings.TEMPLATE_BACKEND_DIR_NAME}/schema.jinja',
            f'{generator_settings.TEMPLATE_BACKEND_DIR_NAME}/service.jinja',
        ]

    @staticmethod
    def get_code_gen_paths(business: GenBusiness) -> list[str]:
        """
        获取代码生成路径列表

        :param business:
        :return:
        """
        app_name = business.app_name
        module_name = business.table_name_en
        target_files = [
            f'{generator_settings.TEMPLATE_BACKEND_DIR_NAME}/{app_name}/api/{business.api_version}/{module_name}.py',
            f'{generator_settings.TEMPLATE_BACKEND_DIR_NAME}/{app_name}/crud/crud_{module_name}.py',
            f'{generator_settings.TEMPLATE_BACKEND_DIR_NAME}/{app_name}/model/{module_name}.py',
            f'{generator_settings.TEMPLATE_BACKEND_DIR_NAME}/{app_name}/schema/{module_name}.py',
            f'{generator_settings.TEMPLATE_BACKEND_DIR_NAME}/{app_name}/service/{module_name}_service.py',
        ]
        return target_files

    def get_code_gen_path(self, tpl_path: str, business: GenBusiness) -> str:
        """
        获取代码生成路径

        :param tpl_path:
        :param business:
        :return:
        """
        target_files = self.get_code_gen_paths(business)
        code_gen_path_mapping = dict(zip(self.get_template_paths(), target_files))
        return code_gen_path_mapping[tpl_path]

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
            'have_datetime_column': business.default_datetime_column,
            'permission_sign': str(business.table_name_en.replace('_', ':')),
            'models': models,
        }


gen_template = GenTemplate()
