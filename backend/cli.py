#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import subprocess

from dataclasses import dataclass
from typing import Annotated, Literal

import cappa
import granian

from cappa import ValueFrom
from rich.panel import Panel
from rich.prompt import IntPrompt
from rich.table import Table
from rich.text import Text
from sqlalchemy import text
from watchfiles import PythonFilter

from backend import console, get_version
from backend.common.enums import DataBaseType, PrimaryKeyType
from backend.common.exception.errors import BaseExceptionMixin
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.plugin.code_generator.schema.code import ImportParam
from backend.plugin.code_generator.service.business_service import gen_business_service
from backend.plugin.code_generator.service.code_service import gen_service
from backend.plugin.tools import get_plugin_sql
from backend.utils._await import run_await
from backend.utils.file_ops import install_git_plugin, install_zip_plugin, parse_sql_script


class CustomReloadFilter(PythonFilter):
    """自定义重载过滤器"""

    def __init__(self):
        super().__init__(extra_extensions=['.json', '.yaml', '.yml'])


def run(host: str, port: int, reload: bool, workers: int) -> None:
    url = f'http://{host}:{port}'
    docs_url = url + settings.FASTAPI_DOCS_URL
    redoc_url = url + settings.FASTAPI_REDOC_URL
    openapi_url = url + (settings.FASTAPI_OPENAPI_URL or '')

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
        reload_filter=CustomReloadFilter,
        workers=workers,
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


async def import_table(
    app: str,
    table_schema: str,
    table_name: str,
) -> None:
    try:
        obj = ImportParam(app=app, table_schema=table_schema, table_name=table_name)
        await gen_service.import_business_and_model(obj=obj)
    except Exception as e:
        raise cappa.Exit(e.msg if isinstance(e, BaseExceptionMixin) else str(e), code=1)


def get_business() -> int:
    ids = []
    try:
        results = run_await(gen_business_service.get_all)()

        if not results:
            raise cappa.Exit('[red]暂无可用的代码生成业务！请先通过 import 命令导入！[/]')

        table = Table(show_header=True, header_style='bold magenta')
        table.add_column('业务编号', style='cyan', no_wrap=True, justify='center')
        table.add_column('应用名称', style='green', no_wrap=True)
        table.add_column('生成路径', style='yellow')
        table.add_column('备注', style='blue')

        for result in results:
            table.add_row(
                str(result.id),
                result.app_name,
                result.gen_path or f'应用 {result.app_name} 根路径',
                result.remark or '',
            )
            ids.append(result.id)

        console.print(table)
    except Exception as e:
        raise cappa.Exit(e.msg if isinstance(e, BaseExceptionMixin) else str(e), code=1)

    business = IntPrompt.ask('请从中选择一个业务编号', choices=[str(_id) for _id in ids])

    return business


def generate(pk: int) -> None:
    try:
        gen_path = run_await(gen_service.generate)(pk=pk)
    except Exception as e:
        raise cappa.Exit(e.msg if isinstance(e, BaseExceptionMixin) else str(e), code=1)

    console.print(Text('\n代码已生成完毕', style='bold green'))
    console.print(Text('\n详情请查看：'), Text(gen_path, style='bold magenta'))


@cappa.command(help='运行 API 服务', default_long=True)
@dataclass
class Run:
    host: Annotated[
        str,
        cappa.Arg(
            default='127.0.0.1',
            help='提供服务的主机 IP 地址，对于本地开发，请使用 `127.0.0.1`。'
            '要启用公共访问，例如在局域网中，请使用 `0.0.0.0`',
        ),
    ]
    port: Annotated[
        int,
        cappa.Arg(default=8000, help='提供服务的主机端口号'),
    ]
    no_reload: Annotated[
        bool,
        cappa.Arg(default=False, help='禁用在（代码）文件更改时自动重新加载服务器'),
    ]
    workers: Annotated[
        int,
        cappa.Arg(default=1, help='使用多个工作进程，必须与 `--no-reload` 同时使用'),
    ]

    def __call__(self):
        run(host=self.host, port=self.port, reload=self.no_reload, workers=self.workers)


@cappa.command(help='从当前主机启动 Celery worker 服务', default_long=True)
@dataclass
class Worker:
    log_level: Annotated[
        Literal['info', 'debug'],
        cappa.Arg(short='-l', default='info', help='日志输出级别'),
    ]

    def __call__(self):
        run_celery_worker(log_level=self.log_level)


@cappa.command(help='从当前主机启动 Celery beat 服务', default_long=True)
@dataclass
class Beat:
    log_level: Annotated[
        Literal['info', 'debug'],
        cappa.Arg(short='-l', default='info', help='日志输出级别'),
    ]

    def __call__(self):
        run_celery_beat(log_level=self.log_level)


@cappa.command(help='从当前主机启动 Celery flower 服务', default_long=True)
@dataclass
class Flower:
    port: Annotated[
        int,
        cappa.Arg(default=8555, help='提供服务的主机端口号'),
    ]
    basic_auth: Annotated[
        str,
        cappa.Arg(default='admin:123456', help='页面登录的用户名和密码'),
    ]

    def __call__(self):
        run_celery_flower(port=self.port, basic_auth=self.basic_auth)


@cappa.command(help='运行 Celery 服务')
@dataclass
class Celery:
    subcmd: cappa.Subcommands[Worker | Beat | Flower]


@cappa.command(help='新增插件', default_long=True)
@dataclass
class Add:
    path: Annotated[
        str | None,
        cappa.Arg(help='ZIP 插件的本地完整路径'),
    ]
    repo_url: Annotated[
        str | None,
        cappa.Arg(help='Git 插件的仓库地址'),
    ]
    no_sql: Annotated[
        bool,
        cappa.Arg(default=False, help='禁用插件 SQL 脚本自动执行'),
    ]
    db_type: Annotated[
        DataBaseType,
        cappa.Arg(default='mysql', help='执行插件 SQL 脚本的数据库类型'),
    ]
    pk_type: Annotated[
        PrimaryKeyType,
        cappa.Arg(default='autoincrement', help='执行插件 SQL 脚本数据库主键类型'),
    ]

    async def __call__(self):
        await install_plugin(self.path, self.repo_url, self.no_sql, self.db_type, self.pk_type)


@cappa.command(help='导入代码生成业务和模型列', default_long=True)
@dataclass
class Import:
    app: Annotated[
        str,
        cappa.Arg(help='应用名称，用于代码生成到指定 app'),
    ]
    table_schema: Annotated[
        str,
        cappa.Arg(short='tc', default='fba', help='数据库名'),
    ]
    table_name: Annotated[
        str,
        cappa.Arg(short='tn', help='数据库表名'),
    ]

    async def __call__(self):
        await import_table(self.app, self.table_schema, self.table_name)


@cappa.command(name='gen', help='代码生成，体验完成功能，请自行部署 fba vben 前端工程！', default_long=True)
@dataclass
class CodeGenerate:
    business: Annotated[
        int,
        cappa.Arg(default=ValueFrom(get_business), help='业务编号'),
    ]
    subcmd: cappa.Subcommands[Import | None] = None

    def __call__(self):
        if self.business:
            generate(self.business)


@cappa.command(help='一个高效的 fba 命令行界面', default_long=True)
@dataclass
class FbaCli:
    version: Annotated[
        bool,
        cappa.Arg(short='-V', default=False, show_default=False, help='打印当前版本号'),
    ]
    sql: Annotated[
        str,
        cappa.Arg(value_name='PATH', default='', show_default=False, help='在事务中执行 SQL 脚本'),
    ]
    subcmd: cappa.Subcommands[Run | Celery | Add | CodeGenerate | None] = None

    async def __call__(self):
        if self.version:
            get_version()
        if self.sql:
            await execute_sql_scripts(self.sql)


def main() -> None:
    output = cappa.Output(error_format='[red]Error[/]: {message}\n\n更多信息，尝试 "[cyan]--help[/]"')
    asyncio.run(cappa.invoke_async(FbaCli, output=output))
