from pathlib import Path

from backend.common.enums import DataBaseType

# 项目根目录
BASE_PATH = Path(__file__).resolve().parent.parent

# 环境变量文件
ENV_FILE_PATH = BASE_PATH / '.env'

# 环境变量示例文件
ENV_EXAMPLE_FILE_PATH = BASE_PATH / '.env.example'

# alembic 迁移文件存放路径
ALEMBIC_VERSION_DIR = BASE_PATH / 'alembic' / 'versions'

# 日志文件路径
LOG_DIR = BASE_PATH / 'log'

# 静态资源目录
STATIC_DIR = BASE_PATH / 'static'

# 上传文件目录
UPLOAD_DIR = STATIC_DIR / 'upload'

# 插件目录
PLUGIN_DIR = BASE_PATH / 'plugin'

# 国际化文件目录
LOCALE_DIR = BASE_PATH / 'locale'

# MySQL 脚本目录
MYSQL_SCRIPT_DIR = BASE_PATH / 'sql' / 'mysql'

# PostgreSQL 脚本目录
POSTGRESQL_SCRIPT_DIR = BASE_PATH / 'sql' / 'postgresql'

# SQL Server 脚本目录
SQLSERVER_SCRIPT_DIR = BASE_PATH / 'sql' / 'sqlserver'


def get_database_sql_dir_name(db_type: DataBaseType) -> str:
    """获取数据库 SQL 目录名称"""
    return db_type.value


def get_database_script_dir(db_type: DataBaseType) -> Path:
    """获取数据库脚本目录"""
    return BASE_PATH / 'sql' / get_database_sql_dir_name(db_type)


# 热重载锁文件
RELOAD_LOCK_FILE = BASE_PATH / '.reload.lock'
