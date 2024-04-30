#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

from backend.core.path_conf import JINJA2_TEMPLATE_DIR


def get_templates(jinja_file: str) -> 'Template':
    """
    获取模版文件

    :param jinja_file:
    :return:
    """
    env = Environment(
        loader=FileSystemLoader(JINJA2_TEMPLATE_DIR),
        autoescape=select_autoescape(['html', 'xml', 'jinja']),
        keep_trailing_newline=True,
    )
    return env.get_template(jinja_file)
