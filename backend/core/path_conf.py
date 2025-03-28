#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

# 项目根目录
BASE_PATH = Path(__file__).resolve().parent.parent

# alembic 迁移文件存放路径
ALEMBIC_VERSION_DIR = BASE_PATH / 'alembic' / 'versions'

# 日志文件路径
LOG_DIR = BASE_PATH / 'log'

# 静态资源目录
STATIC_DIR = BASE_PATH / 'static'

# 上传文件目录
UPLOAD_DIR = STATIC_DIR / 'upload'

# jinja2 模版文件路径
JINJA2_TEMPLATE_DIR = BASE_PATH / 'templates'

# 插件目录
PLUGIN_DIR = BASE_PATH / 'plugin'

# 离线 IP 数据库路径
IP2REGION_XDB = STATIC_DIR / 'ip2region.xdb'
