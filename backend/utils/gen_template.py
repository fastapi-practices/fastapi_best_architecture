#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

from backend.app.generator.model import GenBusiness, GenModel
from backend.core.path_conf import JINJA2_TEMPLATE_DIR


class GenTemplate:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(JINJA2_TEMPLATE_DIR),
            autoescape=select_autoescape(['html', 'xml', 'jinja']),
            trim_blocks=True,
            lstrip_blocks=True,
            enable_async=True,
        )

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
    def get_vars(business: GenBusiness, models: list[GenModel]) -> dict:
        """
        获取模版变量

        :param business:
        :param models:
        :return:
        """
        for model in models:
            pass
        # python 类型对应的 sqla 类型
        model_type_map = {
            'str', 'String',
            'float', 'Float',
            'int', 'Integer',
            'bool', 'Boolean',
        }
        return {
            'app_name': business.app_name,
            'table_name_en': business.table_name_en,
            'table_name_zh': business.table_name_zh,
            'table_simple_name_zh': business.table_simple_name_zh,
            'table_comment': business.table_comment,
            'schema_name': business.schema_name,
            'permission_sign': str(business.__tablename__.replace('_', ':')),
            'models': models,
            'model_type_map': model_type_map,
        }


gen_template = GenTemplate()
