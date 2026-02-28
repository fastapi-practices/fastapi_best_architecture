from rich.console import Console


class CustomConsole(Console):
    """自定义控制台"""

    def info(self, msg: str) -> None:
        """输出信息/进度消息"""
        self.print(f'[bold cyan]•[/] {msg}', highlight=False)

    def success(self, msg: str) -> None:
        """输出成功消息"""
        self.print(f'[bold green]✓[/] [green]{msg}[/]', highlight=False)

    def warning(self, msg: str) -> None:
        """输出警告消息"""
        self.print(f'[bold yellow]⚠[/] [yellow]{msg}[/]', highlight=False)

    def error(self, msg: str) -> None:
        """输出错误消息"""
        self.print(f'[bold red]✗[/] [red]{msg}[/]', highlight=False)


console = CustomConsole()
