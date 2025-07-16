#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import subprocess

from dataclasses import dataclass
from typing import Annotated, Literal

import cappa
import granian

from rich.panel import Panel
from rich.text import Text
from sqlalchemy import text
from watchfiles import PythonFilter

from backend import console, get_version
from backend.common.enums import DataBaseType, PrimaryKeyType
from backend.common.exception.errors import BaseExceptionMixin
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.plugin.tools import get_plugin_sql
from backend.utils.file_ops import install_git_plugin, install_zip_plugin, parse_sql_script


def run(host: str, port: int, reload: bool, workers: int | None) -> None:
    url = f'http://{host}:{port}'
    docs_url = url + settings.FASTAPI_DOCS_URL
    redoc_url = url + settings.FASTAPI_REDOC_URL
    openapi_url = url + settings.FASTAPI_OPENAPI_URL

    panel_content = Text()
    panel_content.append(f'📝 Swagger 文档: {docs_url}\n', style='blue')
    panel_content.append(f'📚 Redoc   文档: {redoc_url}\n', style='yellow')
    panel_content.append(f'📡 OpenAPI JSON: {openapi_url}\n', style='green')
    panel_content.append(
        '🌍 fba 官方文档: https://fastapi-practices.github.io/fastapi_best_architecture_docs/',
        style='cyan',
    )

    console.print(Panel(panel_content, title='fba 服务信息', border_style='purple', padding=(1, 2)))
    granian.Granian(
        target='backend.main:app',
        interface='asgi',
        address=host,
        port=port,
        reload=not reload,
        reload_filter=PythonFilter,
        workers=workers or 1,
    ).serve()


def run_celery_worker(log_level: Literal['info', 'debug']) -> None:
    try:
        subprocess.run(['celery', '-A', 'backend.app.task.celery', 'worker', '-l', f'{log_level}', '-P', 'gevent'])
    except KeyboardInterrupt:
        pass


def run_celery_beat(log_level: Literal['info', 'debug']) -> None:
    try:
        subprocess.run(['celery', '-A', 'backend.app.task.celery', 'beat', '-l', f'{log_level}'])
    except KeyboardInterrupt:
        pass


def run_celery_flower(port: int, basic_auth: str) -> None:
    try:
        subprocess.run([
            'celery',
            '-A',
            'backend.app.task.celery',
            'flower',
            f'--port={port}',
            f'--basic-auth={basic_auth}',
        ])
    except KeyboardInterrupt:
        pass


async def install_plugin(
    path: str, repo_url: str, no_sql: bool, db_type: DataBaseType, pk_type: PrimaryKeyType
) -> None:
    if not path and not repo_url:
        raise cappa.Exit('path 或 repo_url 必须指定其中一项', code=1)
    if path and repo_url:
        raise cappa.Exit('path 和 repo_url 不能同时指定', code=1)

    plugin_name = None
    console.print(Text('开始安装插件...', style='bold cyan'))

    try:
        if path:
            plugin_name = await install_zip_plugin(file=path)
        if repo_url:
            plugin_name = await install_git_plugin(repo_url=repo_url)

        console.print(Text(f'插件 {plugin_name} 安装成功', style='bold green'))

        sql_file = await get_plugin_sql(plugin_name, db_type, pk_type)
        if sql_file and not no_sql:
            console.print(Text('开始自动执行插件 SQL 脚本...', style='bold cyan'))
            await execute_sql_scripts(sql_file)

    except Exception as e:
        raise cappa.Exit(e.msg if isinstance(e, BaseExceptionMixin) else str(e), code=1)


async def execute_sql_scripts(sql_scripts: str) -> None:
    async with async_db_session.begin() as db:
        try:
            stmts = await parse_sql_script(sql_scripts)
            for stmt in stmts:
                await db.execute(text(stmt))
        except Exception as e:
            raise cappa.Exit(f'SQL 脚本执行失败：{e}', code=1)

    console.print(Text('SQL 脚本已执行完成', style='bold green'))


@cappa.command(help='运行 API 服务')
@dataclass
class Run:
    host: Annotated[
        str,
        cappa.Arg(
            long=True,
            default='127.0.0.1',
            help='提供服务的主机 IP 地址，对于本地开发，请使用 `127.0.0.1`。'
            '要启用公共访问，例如在局域网中，请使用 `0.0.0.0`',
        ),
    ]
    port: Annotated[
        int,
        cappa.Arg(long=True, default=8000, help='提供服务的主机端口号'),
    ]
    no_reload: Annotated[
        bool,
        cappa.Arg(long=True, default=False, help='禁用在（代码）文件更改时自动重新加载服务器'),
    ]
    workers: Annotated[
        int | None,
        cappa.Arg(long=True, default=None, help='使用多个工作进程，必须与 `--no-reload` 同时使用'),
    ]

    def __call__(self):
        run(host=self.host, port=self.port, reload=self.no_reload, workers=self.workers)


@cappa.command(help='从当前主机启动 Celery worker 服务')
@dataclass
class Worker:
    log_level: Annotated[
        Literal['info', 'debug'],
        cappa.Arg(long=True, short='-l', default='info', help='日志输出级别'),
    ]

    def __call__(self):
        run_celery_worker(log_level=self.log_level)


@cappa.command(help='从当前主机启动 Celery beat 服务')
@dataclass
class Beat:
    log_level: Annotated[
        Literal['info', 'debug'],
        cappa.Arg(long=True, short='-l', default='info', help='日志输出级别'),
    ]

    def __call__(self):
        run_celery_beat(log_level=self.log_level)


@cappa.command(help='从当前主机启动 Celery flower 服务')
@dataclass
class Flower:
    port: Annotated[int, cappa.Arg(long=True, default=8555, help='提供服务的主机端口号')]
    basic_auth: Annotated[str, cappa.Arg(long=True, default='admin:123456', help='页面登录的用户名和密码')]

    def __call__(self):
        run_celery_flower(port=self.port, basic_auth=self.basic_auth)


@cappa.command(help='运行 Celery 服务')
@dataclass
class Celery:
    subcmd: cappa.Subcommands[Worker | Beat | Flower | None] = None

    def __call__(self):
        console.print('\n更多信息，尝试 "[cyan]--help[/]"')


@cappa.command(help='新增插件')
@dataclass
class Add:
    path: Annotated[
        str | None,
        cappa.Arg(long=True, help='ZIP 插件的本地完整路径'),
    ]
    repo_url: Annotated[
        str | None,
        cappa.Arg(long=True, help='Git 插件的仓库地址'),
    ]
    no_sql: Annotated[
        bool,
        cappa.Arg(long=True, default=False, help='禁用插件 SQL 脚本自动执行'),
    ]
    db_type: Annotated[
        DataBaseType,
        cappa.Arg(long=True, default='mysql', help='执行插件 SQL 脚本的数据库类型'),
    ]
    pk_type: Annotated[
        PrimaryKeyType,
        cappa.Arg(long=True, default='autoincrement', help='执行插件 SQL 脚本数据库主键类型'),
    ]

    async def __call__(self):
        await install_plugin(self.path, self.repo_url, self.no_sql, self.db_type, self.pk_type)


@cappa.command(help='一个高效的 fba 命令行界面')
@dataclass
class FbaCli:
    version: Annotated[
        bool,
        cappa.Arg(short='-V', long=True, default=False, show_default=False, help='打印当前版本号'),
    ]
    sql: Annotated[
        str,
        cappa.Arg(value_name='PATH', long=True, default='', show_default=False, help='在事务中执行 SQL 脚本'),
    ]
    subcmd: cappa.Subcommands[Run | Celery | Add | None] = None

    async def __call__(self):
        if self.version:
            get_version()
        if self.sql:
            await execute_sql_scripts(self.sql)


def main() -> None:
    output = cappa.Output(error_format='[red]Error[/]: {message}\n\n更多信息，尝试 "[cyan]--help[/]"')
    asyncio.run(cappa.invoke_async(FbaCli, output=output))
