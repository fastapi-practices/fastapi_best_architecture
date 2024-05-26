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
            keep_trailing_newline=True,
        )

    def get_template(self, jinja_file: str) -> Template:
        """
        获取模版文件

        :param jinja_file:
        :return:
        """

        return self.env.get_template(jinja_file)

    @staticmethod
    def get_template_paths(self) -> list[str]:
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
        return {
            'app_name': business.app_name,
            'model_name': business.model_name,
            'schema_name': business.schema_name,
            'model_simple_name_zh': business.model_simple_name_zh,
            'permission_sign': str(business.__tablename__.replace('_', ':')),
            # TODO
        }


gen_template = GenTemplate()
