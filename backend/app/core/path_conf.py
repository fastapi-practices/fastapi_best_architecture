#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from pathlib import Path

from backend.app.core.conf import settings

# 获取项目根目录
# 或使用绝对路径，指到backend目录为止，例如windows：BasePath = D:\git_project\fastapi_mysql\backend
BasePath = Path(__file__).resolve().parent.parent.parent

# 迁移文件存放路径
Versions = os.path.join(BasePath, 'app', 'alembic', 'versions')

# 日志文件路径
LogPath = os.path.join(BasePath, 'app', 'log')

# RBAC model.conf 文件路径
RBAC_MODEL_CONF = os.path.join(BasePath, 'app', 'core', settings.CASBIN_RBAC_MODEL_NAME)

# 离线 IP 数据库路径
IP2REGION_XDB = os.path.join(BasePath, 'app', 'static', 'ip2region.xdb')
