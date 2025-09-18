#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os
import shutil
import subprocess

from dataclasses import dataclass
from typing import Annotated, Literal

import cappa
import granian
import questionary

from cappa.output import error_format
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.prompt import IntPrompt
from rich.table import Table
from rich.text import Text
from sqlalchemy import text
from watchfiles import PythonFilter

from backend import __version__
from backend.common.enums import DataBaseType, PrimaryKeyType
from backend.common.exception.errors import BaseExceptionMixin
from backend.core.conf import settings
from backend.core.path_conf import BASE_PATH
from backend.database.db import async_db_session
from backend.plugin.code_generator.schema.code import ImportParam
from backend.plugin.code_generator.service.business_service import gen_business_service
from backend.plugin.code_generator.service.code_service import gen_service
from backend.plugin.tools import get_plugin_sql
from backend.utils._await import run_await
from backend.utils.console import console
from backend.utils.file_ops import install_git_plugin, install_zip_plugin, parse_sql_script

output_help = '\n更多信息，尝试 "[cyan]--help[/]"'


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
    panel_content.append(f'当前版本: v{__version__}')
    panel_content.append(f'\n服务地址: {url}')
    panel_content.append('\n官方文档: https://fastapi-practices.github.io/fastapi_best_architecture_docs/')

    if settings.ENVIRONMENT == 'dev':
        panel_content.append(f'\n\n📖 Swagger 文档: {docs_url}', style='yellow')
        panel_content.append(f'\n📚 Redoc   文档: {redoc_url}', style='blue')
        panel_content.append(f'\n📡 OpenAPI JSON: {openapi_url}', style='green')

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


def generate(gen: bool) -> None:
    if not gen:
        console.print(output_help)
        return

    try:
        ids = []
        results = run_await(gen_business_service.get_all)()

        if not results:
            raise cappa.Exit('[red]暂无可用的代码生成业务！请先通过 import 命令导入！[/]')

        table = Table(show_header=True, header_style='bold magenta')
        table.add_column('业务编号', style='cyan', no_wrap=True, justify='center')
        table.add_column('应用名称', style='green', no_wrap=True)
        table.add_column('生成路径', style='yellow')
        table.add_column('备注', style='blue')

        for result in results:
            ids.append(result.id)
            table.add_row(
                str(result.id),
                result.app_name,
                result.gen_path or f'应用 {result.app_name} 根路径',
                result.remark or '',
            )

        console.print(table)
        business = IntPrompt.ask('请从中选择一个业务编号', choices=[str(_id) for _id in ids])

        gen_path = run_await(gen_service.generate)(pk=business)
    except Exception as e:
        raise cappa.Exit(e.msg if isinstance(e, BaseExceptionMixin) else str(e), code=1)

    console.print(Text('\n代码已生成完毕', style='bold green'))
    console.print(Text('\n详情请查看：'), Text(gen_path, style='bold magenta'))


async def simplify():
    title = Text()
    title.append('🚀 FastAPI Best Architecture · ', style='turquoise4')
    title.append('代码精简程序 ✨', style='medium_purple1')
    content = Text()
    content.append('精简 fba 当前实现，快速切换至新项目开发模式', style='grey50')
    content.append('\n\n🟨 安全警告', style='deep_sky_blue1')
    content.append('\n\n   此操作将永久删除清理列表内容，且无法恢复！', style='gold1')
    content.append('\n   请仔细阅读清理列表，确认后再继续操作', style='grey50')
    content.append('\n\n🟥 清理列表', style='deep_sky_blue1')
    content.append('\n\n   1. 应用模块')
    content.append(
        '\n   admin[monitor、sys/data_rule、sys/data_scope、sys/dept、sys/files、sys/menu、sys/role]', style='grey50'
    )
    content.append('\n   task', style='grey50')
    content.append('\n\n   2. 公共模块')
    content.append('\n   common[security/permission、security/rbac]', style='grey50')
    content.append('\n\n   3. 插件模块')
    content.append('\n   plugin[code_generator、config、dict、notice]', style='grey50')
    content.append('\n\n   4. 工具模块')
    content.append('\n   utils[redis_info、server_info]', style='grey50')
    content.append('\n\n   4. Git模块')
    content.append('\n   Git[.github]', style='grey50')
    content.append('\n\n🟩 默认保留', style='deep_sky_blue1')
    content.append('\n\n   1. 应用模块')
    content.append('\n   admin[auth、log、sys/user、sys/plugin]', style='grey50')
    content.append('\n\n   2. 公共模块')
    content.append('\n   除清理列表已选择外所有', style='grey50')
    content.append('\n\n   3. 插件模块')
    content.append('\n   除清理列表已选择外所有', style='grey50')
    content.append('\n\n   4. 工具模块')
    content.append('\n   除清理列表已选择外所有', style='grey50')
    content.append('\n\n   5. 其他模块')
    content.append('\n   除清理列表已选择外所有', style='grey50')
    console.print(Panel(content, title=title, expand=False, padding=(1, 2)))

    go = await questionary.confirm('确认继续吗？', qmark='🟨').ask_async()
    if not go:
        return

    ego = await questionary.confirm('真的确认继续吗？', qmark='🟨').ask_async()
    if not ego:
        return

    # 定义可选可清理列表
    del_list = [
        'admin[monitor、sys/data_rule、sys/data_scope、sys/dept、sys/files、sys/menu、sys/role]',
        'task',
        'common[security/permission、security/rbac]',
        'plugin[code_generator]',
        'plugin[config]',
        'plugin[dict]',
        'plugin[notice]',
        'utils[redis_info、server_info]',
        'Git[.github]',
    ]

    console.print(f'\n🟨 开始清理，共 {len(del_list)} 个模块需要处理...\n')

    def remove_file(paths: list[str]):
        for path in paths:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

    def remove_module(value: str):
        match value:
            case 'admin[monitor、sys/data_rule、sys/data_scope、sys/dept、sys/files、sys/menu、sys/role]':
                remove_file([
                    os.path.join(BASE_PATH, 'admin', 'api', 'v1', 'monitor'),
                    os.path.join(BASE_PATH, 'admin', 'api', 'v1', 'sys', 'data_rule.py'),
                    os.path.join(BASE_PATH, 'admin', 'crud', 'crud_data_rule.py'),
                    os.path.join(BASE_PATH, 'admin', 'model', 'data_rule.py'),
                    os.path.join(BASE_PATH, 'admin', 'schema', 'data_rule.py'),
                    os.path.join(BASE_PATH, 'admin', 'service', 'data_rule_service.py'),
                    os.path.join(BASE_PATH, 'admin', 'api', 'v1', 'sys', 'data_scope.py'),
                    os.path.join(BASE_PATH, 'admin', 'crud', 'crud_data_scope.py'),
                    os.path.join(BASE_PATH, 'admin', 'model', 'data_scope.py'),
                    os.path.join(BASE_PATH, 'admin', 'schema', 'data_scope.py'),
                    os.path.join(BASE_PATH, 'admin', 'service', 'data_scope_service.py'),
                    os.path.join(BASE_PATH, 'admin', 'api', 'v1', 'sys', 'dept.py'),
                    os.path.join(BASE_PATH, 'admin', 'crud', 'crud_dept.py'),
                    os.path.join(BASE_PATH, 'admin', 'model', 'dept.py'),
                    os.path.join(BASE_PATH, 'admin', 'schema', 'dept.py'),
                    os.path.join(BASE_PATH, 'admin', 'service', 'dept_service.py'),
                    os.path.join(BASE_PATH, 'admin', 'api', 'v1', 'sys', 'files.py'),
                    os.path.join(BASE_PATH, 'admin', 'api', 'v1', 'sys', 'menu.py'),
                    os.path.join(BASE_PATH, 'admin', 'crud', 'crud_menu.py'),
                    os.path.join(BASE_PATH, 'admin', 'model', 'menu.py'),
                    os.path.join(BASE_PATH, 'admin', 'schema', 'menu.py'),
                    os.path.join(BASE_PATH, 'admin', 'service', 'menu_service.py'),
                    os.path.join(BASE_PATH, 'admin', 'api', 'v1', 'sys', 'role.py'),
                    os.path.join(BASE_PATH, 'admin', 'crud', 'crud_role.py'),
                    os.path.join(BASE_PATH, 'admin', 'model', 'role.py'),
                    os.path.join(BASE_PATH, 'admin', 'schema', 'role.py'),
                    os.path.join(BASE_PATH, 'admin', 'service', 'role_service.py'),
                ])

            case 'task':
                remove_file([os.path.join(BASE_PATH, 'app', 'task')])

            case 'common[security/permission、security/rbac]':
                remove_file([
                    os.path.join(BASE_PATH, 'common', 'security', 'permission.py'),
                    os.path.join(BASE_PATH, 'common', 'security', 'rbac.py'),
                ])

            case 'plugin[code_generator]':
                remove_file([os.path.join(BASE_PATH, 'plugin', 'code_generator')])

            case 'plugin[config]':
                remove_file([os.path.join(BASE_PATH, 'plugin', 'config')])

            case 'plugin[dict]':
                remove_file([os.path.join(BASE_PATH, 'plugin', 'dict')])

            case 'plugin[notice]':
                remove_file([os.path.join(BASE_PATH, 'plugin', 'notice')])

            case 'utils[redis_info、server_info]':
                remove_file([
                    os.path.join(BASE_PATH, 'utils', 'redis_info.py'),
                    os.path.join(BASE_PATH, 'utils', 'server_info.py'),
                ])
            case 'Git[.github]':
                remove_file([
                    os.path.join(BASE_PATH.parent, '.github'),
                ])

    with Progress(
        SpinnerColumn(finished_text='🟩 [bold cyan]清理完成[/]'),
        TextColumn('{task.completed}/{task.total}', style='bold green'),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task('[cyan]正在清理模块...', total=len(del_list))

        for v in del_list:
            remove_module(v)
            await asyncio.sleep(0.5)
            progress.advance(task)

    console.print('\n✨  项目已准备就绪！🚀', style='bold green')
    console.print('\n🟨 当前并未实现全局清理，仍需自行清理', style='bold yellow')


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


@cappa.command(name='codegen', help='代码生成（体验完整功能，请自行部署 fba vben 前端工程）', default_long=True)
@dataclass
class CodeGenerate:
    gen: Annotated[
        bool,
        cappa.Arg(default=False, show_default=False, help='执行代码生成'),
    ]
    subcmd: cappa.Subcommands[Import | None] = None

    def __call__(self):
        generate(self.gen)


@cappa.command(help='一个高效的 fba 命令行界面', default_long=True)
@dataclass
class FbaCli:
    sql: Annotated[
        str,
        cappa.Arg(value_name='PATH', default='', show_default=False, help='在事务中执行 SQL 脚本'),
    ]
    simplify: Annotated[bool, cappa.Arg(default=False, help='精简 fba 当前实现，快速切换至新项目开发模式')]
    subcmd: cappa.Subcommands[Run | Celery | Add | CodeGenerate | None] = None

    async def __call__(self):
        if self.sql:
            await execute_sql_scripts(self.sql)
        if self.simplify:
            await simplify()


def main() -> None:
    output = cappa.Output(error_format=f'{error_format}\n{output_help}')
    asyncio.run(cappa.invoke_async(FbaCli, version=__version__, output=output))
