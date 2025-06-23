import os
from typing import Union

from rich.console import Console

from .models import PaperData


def get_terminal_width() -> int:
    try:
        width = os.get_terminal_size().columns
        if not width or not isinstance(width, int):
            width = 80
        return width
    except Exception:
        return 80


class CustomConsole:
    def __init__(self):
        self.console = Console()
        self.width = get_terminal_width()
        self.verbose_level = 2
        self.level_map = {
            "silent": 0,  # try not to produce anything in stdout nor stderr
            "minimal": 1,  # only print errors & final result
            "default": 2,  # print errors and standard info
            "verbose": 3,  # print everything including paper info
        }

    def set_verbose_level(self, level: Union[str, int] = "default"):
        """
        Setting verbose level for the custom console.

        Args:
            level (Union[str, int]): The verbose level to set.
                - "silent": 0
                - "minimal": 1
                - "default": 2
                - "verbose": 3
                - int: 0-3

        Returns:
            None

        Raises:
            Never throws an error by design, it will fallback to the default level if any invalid input is provided.
        """
        if isinstance(level, int):
            if 0 <= level <= 3:
                self.verbose_level = level
            else:
                self.verbose_level = 2
        elif isinstance(level, str):
            level = str(level).lower()
            self.verbose_level = self.level_map.get(level, 2)
        else:
            self.verbose_level = 2

    def print(self, *args, **kwargs):
        self.console.print(*args, **kwargs)

    ###########################################################################
    ### Keep it minimal

    def error(self, text: str):
        if self.verbose_level >= 1:
            self.console.print("[red]✗ " + text)

    def success(self, text: str):
        if self.verbose_level >= 1:
            self.console.print("[green]✓ " + text)

    ###########################################################################
    ### Standard

    def info(self, text: str):
        if self.verbose_level >= 2:
            self.console.print("[green dim]> " + text)

    def process(self, i: int, total: int, target: str):
        if self.verbose_level >= 2:
            # self.console.print(
            #     f"[white bold][{i+1}/{total}][/white bold] >>> [white dim]{target}"
            # )
            # self.console.print(f"[green dim]> Target [{i+1}/{total}] >>> {target}")
            self.console.print(f"[green dim]> Target [{i+1}/{total}]: {target}")

    ###########################################################################
    ### Verbose

    def warn(self, text: str):
        if self.verbose_level >= 3:
            self.console.print("[yellow]⚠️ " + text)

    def debug(self, text: str):
        if self.verbose_level >= 3:
            self.console.print("[blue]" + text)

    def print_paper_info(self, paper_data: PaperData):
        if self.verbose_level >= 3:
            # self.print(paper_data.model_dump())
            self.print("[cyan dim]" + "+" * self.width)
            self.print(f"  [dim]Paper Title  :[/dim] [green bold]{paper_data.title}")
            self.print(
                f"  [dim]Authors      :[/dim] [green bold]{', '.join(paper_data.authors)}"
            )
            self.print(f"  [dim]Abstract     :[/dim] [green]{paper_data.abstract}")
            self.print(f"  [dim]Abstract URL :[/dim] [blue]{paper_data.abs_url}")
            self.print(f"  [dim]PDF URL      :[/dim] [blue]{paper_data.pdf_url}")
            self.print("[cyan dim]" + "+" * self.width)


console = CustomConsole()
