#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Annotated

import uvicorn

from cappa import Arg, Subcommands, invoke
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.text import Text

from backend import console, get_version
from backend.core.conf import settings
from backend.plugin.tools import get_plugins, install_requirements


def run(host: str, port: int, reload: bool, workers: int | None) -> None:
    console.print(Text('检测插件依赖...', style='bold cyan'))

    plugins = get_plugins()

    with Progress(
        SpinnerColumn(finished_text='[bold green]插件依赖安装完成[/]'),
        TextColumn('[green]{task.completed}/{task.total}[/]'),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task('安装插件依赖...', total=len(plugins))
        for i, plugin in enumerate(plugins):
            install_requirements(plugin)
            progress.advance(task)

    url = f'http://{host}:{port}'
    docs_url = url + settings.FASTAPI_DOCS_URL
    redoc_url = url + settings.FASTAPI_REDOC_URL
    openapi_url = url + settings.FASTAPI_OPENAPI_URL

    console.print(Text('启动 fba 服务...', style='bold magenta'))

    panel_content = Text()
    panel_content.append(f'📝 Swagger 文档: {docs_url}\n', style='blue')
    panel_content.append(f'📚 Redoc   文档: {redoc_url}\n', style='yellow')
    panel_content.append(f'📡 OpenAPI JSON: {openapi_url}\n', style='green')
    panel_content.append(
        '🌍 fba 官方文档: https://fastapi-practices.github.io/fastapi_best_architecture_docs/',
        style='cyan',
    )

    console.print(Panel(panel_content, title='fba 服务信息', border_style='purple', padding=(1, 2)))
    uvicorn.run(app='backend.main:app', host=host, port=port, reload=reload, workers=workers)


@dataclass
class Run:
    host: Annotated[
        str,
        Arg(
            long=True,
            default='127.0.0.1',
            help='提供服务的主机 IP 地址，对于本地开发，请使用 `127.0.0.1`。'
            '要启用公共访问，例如在局域网中，请使用 `0.0.0.0`',
        ),
    ]
    port: Annotated[
        int,
        Arg(long=True, default=8000, help='提供服务的主机端口号'),
    ]
    reload: Annotated[
        bool,
        Arg(long=True, default=True, help='启用在（代码）文件更改时自动重新加载服务器'),
    ]
    workers: Annotated[
        int | None,
        Arg(long=True, default=None, help='使用多个工作进程。与 `--reload` 标志互斥'),
    ]

    def __call__(self):
        run(host=self.host, port=self.port, reload=self.reload, workers=self.workers)


@dataclass
class FbaCli:
    version: Annotated[
        bool,
        Arg(short='-V', long=True, default=False, help='打印 fba 当前版本号'),
    ]
    subcmd: Subcommands[Run | None] = None

    def __call__(self):
        if self.version:
            get_version()


def main() -> None:
    invoke(FbaCli)
