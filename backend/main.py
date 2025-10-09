from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.text import Text

from backend.core.registrar import register_app
from backend.plugin.tools import get_plugins, install_requirements
from backend.utils.console import console
from backend.utils.timezone import timezone

_log_prefix = f'{timezone.to_str(timezone.now(), "%Y-%m-%d %H:%M:%S.%M0")} | {"INFO": <8} | - | '
console.print(Text(f'{_log_prefix}检测插件依赖...', style='bold cyan'))

_plugins = get_plugins()

with Progress(
    SpinnerColumn(finished_text=f'[bold green]{_log_prefix}插件准备就绪[/]'),
    TextColumn('{task.description}'),
    TextColumn('{task.completed}/{task.total}', style='bold green'),
    TimeElapsedColumn(),
    console=console,
) as progress:
    task = progress.add_task('安装插件依赖...', total=len(_plugins))
    for plugin in _plugins:
        progress.update(task, description=f'[bold magenta]安装插件 {plugin} 依赖...[/]')
        install_requirements(plugin)
        progress.advance(task)
    progress.update(task, description='[bold green]-[/]')

console.print(Text(f'{_log_prefix}启动服务...', style='bold magenta'))

app = register_app()
