from rich.console import Console


class CustomConsole(Console):
    """自定义控制台"""

    def note(self, msg: str) -> None:
        """输出注释"""
        self.print(f'[bold white]•[/] [white]{msg}[/]')

    def info(self, msg: str) -> None:
        """输出信息"""
        self.print(f'[bold cyan]•[/] {msg}')

    def tip(self, msg: str) -> None:
        """输出提示消息"""
        self.print(f'[bold green]✓[/] [green]{msg}[/]')

    def warning(self, msg: str) -> None:
        """输出警告消息"""
        self.print(f'[bold yellow]⚠[/] [yellow]{msg}[/]')

    def caution(self, msg: str) -> None:
        """输出危险消息"""
        self.print(f'[bold red]✗[/] [red]{msg}[/]')


console = CustomConsole()
