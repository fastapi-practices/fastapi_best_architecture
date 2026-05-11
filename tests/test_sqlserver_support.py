from pytest import MonkeyPatch
from sqlalchemy import URL

from backend.common.enums import DataBaseType
from backend.core.conf import settings
from backend.core.path_conf import get_database_script_dir, get_database_sql_dir_name
from backend.database.db import create_database_url


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


def test_database_script_dir_resolves_all_database_types() -> None:
    assert get_database_sql_dir_name(DataBaseType.mysql) == 'mysql'
    assert get_database_sql_dir_name(DataBaseType.postgresql) == 'postgresql'
    assert get_database_sql_dir_name(DataBaseType.sqlserver) == 'sqlserver'
    assert get_database_script_dir(DataBaseType.sqlserver).as_posix().endswith('/sql/sqlserver')
