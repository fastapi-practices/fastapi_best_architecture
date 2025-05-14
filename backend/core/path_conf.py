#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

# Project Root Directory
BASE_PATH = Path(__file__).resolve().parent.parent

# alembic migration file storage path
ALEMBIC_VERSION_DIR = BASE_PATH / 'alembic' / 'versions'

# Log File Path
LOG_DIR = BASE_PATH / 'log'

# Static Resource Directory
STATIC_DIR = BASE_PATH / 'static'

# Upload File Directory
UPLOAD_DIR = STATIC_DIR / 'upload'

# Plugin Directory
PLUGIN_DIR = BASE_PATH / 'plugin'

# OFFLINE IP DATABASE PATH
IP2REGION_XDB = STATIC_DIR / 'ip2region.xdb'
