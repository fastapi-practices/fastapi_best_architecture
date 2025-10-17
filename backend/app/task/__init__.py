import sys

from backend.core.path_conf import BASE_PATH

from .actions import *  # noqa: F403

# 导入项目根目录
sys.path.append(str(BASE_PATH.parent))
