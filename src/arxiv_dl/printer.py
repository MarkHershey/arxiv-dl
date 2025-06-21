import os
from typing import Union

from rich.console import Console

from .models import PaperData


class CustomConsole:
    def __init__(self):
        self.console = Console()
        self.verbose_level = 2
        self.width = os.get_terminal_size().columns
        self.level_map = {
            "silent": 0,  # try not to produce anything in stdout nor stderr
            "minimal": 1,  # only print errors & final result
            "default": 2,  # print errors and standard info
            "verbose": 3,  # print everything including paper info
        }

    def set_verbose_level(self, level: Union[str, int] = "default"):
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

    def lookup(self, text: str):
        if self.verbose_level >= 2:
            self.console.print("[green dim]> " + text)

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
            self.print(f"  Paper Title  : [green bold]{paper_data.title}")
            self.print(f"  Authors      : [green bold]{', '.join(paper_data.authors)}")
            self.print(f"  Abstract     : [green]{paper_data.abstract}")
            self.print(f"  Abstract URL : [blue]{paper_data.abs_url}")
            self.print(f"  PDF URL      : [blue]{paper_data.pdf_url}")
            self.print("[cyan dim]" + "+" * self.width)


console = CustomConsole()
