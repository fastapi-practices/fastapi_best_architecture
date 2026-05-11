import asyncio

from pathlib import Path

from pytest import MonkeyPatch
from sqlalchemy import URL
from sqlalchemy.sql.elements import TextClause

import backend.cli as cli

from backend.cli import (
    _get_database_prompt_defaults,
    _validate_database_schema_name,
    create_database,
    setup_env_file,
)
from backend.common.enums import DataBaseType, PrimaryKeyType
from backend.core.conf import settings
from backend.core.path_conf import get_database_script_dir, get_database_sql_dir_name
from backend.database.db import create_database_url
from backend.plugin.core import get_plugin_sql
from backend.utils.sql_parser import parse_sql_script

_ENV_EXAMPLE_CONTENT = """ENVIRONMENT='dev'
DATABASE_TYPE='postgresql'
DATABASE_HOST='127.0.0.1'
DATABASE_PORT=5432
DATABASE_USER='postgres'
DATABASE_PASSWORD='123456'
DATABASE_DRIVER='ODBC Driver 18 for SQL Server'
DATABASE_TRUST_SERVER_CERTIFICATE=true
REDIS_HOST='127.0.0.1'
REDIS_PORT=6379
REDIS_PASSWORD=''
REDIS_DATABASE=0
TOKEN_SECRET_KEY='old'
"""


class _FakeResult:
    def __init__(self, *, exists: bool) -> None:
        self.exists = exists

    def fetchone(self) -> tuple[int] | None:
        return (1,) if self.exists else None


class _FakeConnection:
    def __init__(self) -> None:
        self.statements: list[str] = []

    async def execute(self, statement: TextClause) -> _FakeResult:
        sql = str(statement)
        self.statements.append(sql)
        return _FakeResult(exists='sys.databases' in sql)


class _UnexpectedPromptError(AssertionError):
    pass


def _write_env_example(tmp_path: Path) -> tuple[Path, Path]:
    env_example_path = tmp_path / '.env.example'
    env_file_path = tmp_path / '.env'
    env_example_path.write_text(_ENV_EXAMPLE_CONTENT, encoding='utf-8')
    return env_example_path, env_file_path


def test_sqlserver_enum_value_exists() -> None:
    assert DataBaseType.sqlserver == 'sqlserver'


def test_create_database_url_uses_aioodbc_for_sqlserver(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(settings, 'DATABASE_TYPE', DataBaseType.sqlserver)
    monkeypatch.setattr(settings, 'DATABASE_HOST', 'sqlserver.local')
    monkeypatch.setattr(settings, 'DATABASE_PORT', 1433)
    monkeypatch.setattr(settings, 'DATABASE_USER', 'sa')
    monkeypatch.setattr(settings, 'DATABASE_PASSWORD', 'Passw0rd!')
    monkeypatch.setattr(settings, 'DATABASE_SCHEMA', 'fba')
    monkeypatch.setattr(settings, 'DATABASE_DRIVER', 'ODBC Driver 18 for SQL Server', raising=False)
    monkeypatch.setattr(settings, 'DATABASE_TRUST_SERVER_CERTIFICATE', True, raising=False)

    url = create_database_url()

    assert isinstance(url, URL)
    assert url.drivername == 'mssql+aioodbc'
    assert url.username == 'sa'
    assert url.password == 'Passw0rd!'
    assert url.host == 'sqlserver.local'
    assert url.port == 1433
    assert url.database == 'fba'
    assert url.query['driver'] == 'ODBC Driver 18 for SQL Server'
    assert url.query['TrustServerCertificate'] == 'yes'
    assert url.query['LongAsMax'] == 'Yes'


def test_create_database_url_uses_master_when_sqlserver_database_is_omitted(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(settings, 'DATABASE_TYPE', DataBaseType.sqlserver)
    monkeypatch.setattr(settings, 'DATABASE_HOST', '127.0.0.1')
    monkeypatch.setattr(settings, 'DATABASE_PORT', 1433)
    monkeypatch.setattr(settings, 'DATABASE_USER', 'sa')
    monkeypatch.setattr(settings, 'DATABASE_PASSWORD', 'Passw0rd!')
    monkeypatch.setattr(settings, 'DATABASE_SCHEMA', 'fba')
    monkeypatch.setattr(settings, 'DATABASE_DRIVER', 'ODBC Driver 18 for SQL Server', raising=False)
    monkeypatch.setattr(settings, 'DATABASE_TRUST_SERVER_CERTIFICATE', False, raising=False)

    url = create_database_url(with_database=False)

    assert url.drivername == 'mssql+aioodbc'
    assert url.database == 'master'
    assert url.query['TrustServerCertificate'] == 'no'


def test_database_script_dir_accepts_string_database_type() -> None:
    assert get_database_sql_dir_name('mysql') == 'mysql'
    assert get_database_sql_dir_name('postgresql') == 'postgresql'
    assert get_database_sql_dir_name('sqlserver') == 'sqlserver'
    assert get_database_script_dir('postgresql').as_posix().endswith('/sql/postgresql')


def test_database_prompt_defaults_include_sqlserver() -> None:
    assert _get_database_prompt_defaults(DataBaseType.mysql) == ('3306', 'root')
    assert _get_database_prompt_defaults(DataBaseType.postgresql) == ('5432', 'postgres')
    assert _get_database_prompt_defaults(DataBaseType.sqlserver) == ('1433', 'sa')
    assert _get_database_prompt_defaults('sqlserver') == ('1433', 'sa')


def test_setup_env_file_updates_sqlserver_env_and_settings(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    env_example_path, env_file_path = _write_env_example(tmp_path)
    prompt_answers = {
        '数据库类型': 'sqlserver',
        '数据库主机': '10.0.0.5',
        '数据库端口': '1433',
        '数据库用户名': 'sa',
        '数据库密码': 'Passw0rd!',
        'SQL Server ODBC Driver': 'ODBC Driver 18 for SQL Server',
        '是否信任 SQL Server 服务器证书': 'false',
        'Redis 主机': '127.0.0.1',
        'Redis 端口': '6379',
        'Redis 密码（留空表示无密码）': '',
        'Redis 数据库编号': '0',
    }

    def fake_prompt_ask(question: str, **kwargs: object) -> str:
        if question == '是否信任 SQL Server 服务器证书':
            assert kwargs['default'] == 'false'
        return prompt_answers[question]

    monkeypatch.setattr(cli, 'ENV_EXAMPLE_FILE_PATH', env_example_path)
    monkeypatch.setattr(cli, 'ENV_FILE_PATH', env_file_path)
    monkeypatch.setattr(cli.Prompt, 'ask', fake_prompt_ask)
    monkeypatch.setattr(cli.secrets, 'token_urlsafe', lambda _: 'fixed-token')
    monkeypatch.setattr(settings, 'DATABASE_DRIVER', 'ODBC Driver 18 for SQL Server', raising=False)
    monkeypatch.setattr(settings, 'DATABASE_TRUST_SERVER_CERTIFICATE', False, raising=False)

    assert setup_env_file() is True

    generated_env = env_file_path.read_text(encoding='utf-8')
    assert "DATABASE_TYPE='sqlserver'" in generated_env
    assert "DATABASE_HOST='10.0.0.5'" in generated_env
    assert 'DATABASE_PORT=1433' in generated_env
    assert "DATABASE_USER='sa'" in generated_env
    assert "DATABASE_PASSWORD='Passw0rd!'" in generated_env
    assert "DATABASE_DRIVER='ODBC Driver 18 for SQL Server'" in generated_env
    assert 'DATABASE_TRUST_SERVER_CERTIFICATE=false' in generated_env
    assert "TOKEN_SECRET_KEY='fixed-token'" in generated_env
    assert settings.DATABASE_TYPE == 'sqlserver'
    assert settings.DATABASE_HOST == '10.0.0.5'
    assert settings.DATABASE_PORT == '1433'
    assert settings.DATABASE_USER == 'sa'
    assert settings.DATABASE_PASSWORD == 'Passw0rd!'
    assert settings.DATABASE_DRIVER == 'ODBC Driver 18 for SQL Server'
    assert settings.DATABASE_TRUST_SERVER_CERTIFICATE is False
    assert settings.REDIS_HOST == '127.0.0.1'
    assert settings.REDIS_PORT == '6379'
    assert not settings.REDIS_PASSWORD
    assert settings.REDIS_DATABASE == '0'
    assert settings.TOKEN_SECRET_KEY == 'fixed-token'


def test_setup_env_file_skips_sqlserver_only_prompts_for_postgresql(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    env_example_path, env_file_path = _write_env_example(tmp_path)
    prompt_answers = {
        '数据库类型': 'postgresql',
        '数据库主机': '127.0.0.1',
        '数据库端口': '5432',
        '数据库用户名': 'postgres',
        '数据库密码': '123456',
        'Redis 主机': '127.0.0.1',
        'Redis 端口': '6379',
        'Redis 密码（留空表示无密码）': '',
        'Redis 数据库编号': '0',
    }
    asked_questions: list[str] = []

    def fake_prompt_ask(question: str, **_: object) -> str:
        asked_questions.append(question)
        if question in {'SQL Server ODBC Driver', '是否信任 SQL Server 服务器证书'}:
            raise _UnexpectedPromptError(question)
        return prompt_answers[question]

    monkeypatch.setattr(cli, 'ENV_EXAMPLE_FILE_PATH', env_example_path)
    monkeypatch.setattr(cli, 'ENV_FILE_PATH', env_file_path)
    monkeypatch.setattr(cli.Prompt, 'ask', fake_prompt_ask)
    monkeypatch.setattr(cli.secrets, 'token_urlsafe', lambda _: 'fixed-token')
    monkeypatch.setattr(settings, 'DATABASE_DRIVER', 'ODBC Driver 18 for SQL Server', raising=False)
    monkeypatch.setattr(settings, 'DATABASE_TRUST_SERVER_CERTIFICATE', True, raising=False)

    assert setup_env_file() is True

    generated_env = env_file_path.read_text(encoding='utf-8')
    assert "DATABASE_TYPE='postgresql'" in generated_env
    assert "DATABASE_DRIVER='ODBC Driver 18 for SQL Server'" in generated_env
    assert 'DATABASE_TRUST_SERVER_CERTIFICATE=true' in generated_env
    assert 'SQL Server ODBC Driver' not in asked_questions
    assert '是否信任 SQL Server 服务器证书' not in asked_questions


def test_validate_database_schema_name_accepts_valid_sqlserver_name() -> None:
    assert _validate_database_schema_name('fba_2026') == 'fba_2026'


def test_create_database_recreates_sqlserver_database(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(settings, 'DATABASE_TYPE', DataBaseType.sqlserver)
    monkeypatch.setattr(settings, 'DATABASE_SCHEMA', 'fba')
    conn = _FakeConnection()

    assert asyncio.run(create_database(conn)) is True
    assert conn.statements == [
        "SELECT 1 FROM sys.databases WHERE name = N'fba'",
        'ALTER DATABASE [fba] SET SINGLE_USER WITH ROLLBACK IMMEDIATE',
        'DROP DATABASE [fba]',
        'CREATE DATABASE [fba]',
    ]


def test_create_database_uses_validated_sqlserver_schema(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(settings, 'DATABASE_TYPE', DataBaseType.sqlserver)
    monkeypatch.setattr(settings, 'DATABASE_SCHEMA', 'fba_2026')
    conn = _FakeConnection()

    assert asyncio.run(create_database(conn)) is True
    assert conn.statements == [
        "SELECT 1 FROM sys.databases WHERE name = N'fba_2026'",
        'ALTER DATABASE [fba_2026] SET SINGLE_USER WITH ROLLBACK IMMEDIATE',
        'DROP DATABASE [fba_2026]',
        'CREATE DATABASE [fba_2026]',
    ]


def test_create_database_rejects_invalid_sqlserver_schema(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(settings, 'DATABASE_TYPE', DataBaseType.sqlserver)
    monkeypatch.setattr(settings, 'DATABASE_SCHEMA', 'fba];DROP_DATABASE_x')
    conn = _FakeConnection()

    assert asyncio.run(create_database(conn)) is False
    assert conn.statements == []


def test_parse_sql_script_accepts_sqlserver_init_prefixes(tmp_path: Path) -> None:
    sql_file = tmp_path / 'init.sql'
    sql_file.write_text(
        """
DECLARE @menu_id bigint;
SET @menu_id = 1;
INSERT INTO sys_menu (id, name) VALUES (1, 'Demo');
DBCC CHECKIDENT ('sys_menu', RESEED, 1);
SELECT 1;
""".strip(),
        encoding='utf-8',
    )

    statements = asyncio.run(parse_sql_script(str(sql_file)))

    assert statements == [
        'DECLARE @menu_id bigint;',
        'SET @menu_id = 1;',
        "INSERT INTO sys_menu (id, name) VALUES (1, 'Demo');",
        "DBCC CHECKIDENT ('sys_menu', RESEED, 1);",
        'SELECT 1;',
    ]


def test_plugin_sql_lookup_accepts_string_database_type_for_existing_database() -> None:
    init_sql = asyncio.run(get_plugin_sql('dict', 'postgresql', PrimaryKeyType.autoincrement))

    assert init_sql is not None
    assert init_sql.replace('\\', '/').endswith('/backend/plugin/dict/sql/postgresql/init.sql')
