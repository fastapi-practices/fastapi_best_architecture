#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os

from dataclasses import dataclass
from typing import Annotated

import cappa
import uvicorn

from rich.panel import Panel
from rich.text import Text

from backend import console, get_version
from backend.common.exception.errors import BaseExceptionMixin
from backend.core.conf import settings
from backend.utils.file_ops import install_git_plugin, install_zip_plugin


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
    uvicorn.run(
        app='backend.main:app',
        host=host,
        port=port,
        reload=not reload,
        reload_excludes=[os.path.abspath('../.venv' if 'backend' in os.getcwd() else '.venv')],
        workers=workers,
    )


async def install_plugin(path: str, repo_url: str) -> None:
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
    except Exception as e:
        raise cappa.Exit(e.msg if isinstance(e, BaseExceptionMixin) else str(e), code=1)

    console.print(Text(f'插件 {plugin_name} 安装成功', style='bold cyan'))


@cappa.command(help='运行服务')
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

    async def __call__(self):
        await install_plugin(path=self.path, repo_url=self.repo_url)


@dataclass
class FbaCli:
    version: Annotated[
        bool,
        cappa.Arg(short='-V', long=True, default=False, help='打印当前版本号'),
    ]
    subcmd: cappa.Subcommands[Run | Add | None] = None

    def __call__(self):
        if self.version:
            get_version()


def main() -> None:
    output = cappa.Output(error_format='[red]Error[/]: {message}\n\n更多信息，尝试 "[cyan]--help[/]"')
    asyncio.run(cappa.invoke_async(FbaCli, output=output))
