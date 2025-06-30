#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.text import Text

from backend import console
from backend.core.registrar import register_app
from backend.plugin.tools import get_plugins, install_requirements
from backend.utils.timezone import timezone

_print_log_style = f'{timezone.to_str(timezone.now(), "%Y-%m-%d %H:%M:%S.%M0")} | fba      |  -  | '
console.print(Text(f'{_print_log_style}检测插件依赖...', style='bold cyan'))

_plugins = get_plugins()

with Progress(
    SpinnerColumn(finished_text=f'[bold green]{_print_log_style}插件准备就绪[/]'),
    TextColumn('[bold green]{task.completed}/{task.total}[/]'),
    TimeElapsedColumn(),
    console=console,
) as progress:
    task = progress.add_task('安装插件依赖...', total=len(_plugins))
    for plugin in _plugins:
        install_requirements(plugin)
        progress.advance(task)

console.print(Text(f'{_print_log_style}启动服务...', style='bold magenta'))

app = register_app()
