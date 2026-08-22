import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.style import Style
from rich.theme import Theme

# Custom Theme: Murni Merah, Hijau, Kuning, Putih
custom_theme = Theme(
    {
        "markdown.paragraph": "bold white",
        "markdown.text": "white",
        "markdown.heading": "bold yellow",
        "markdown.code": "bold yellow",
        "markdown.code_block": "bold white",
        "markdown.item": "white",
        "markdown.bold": "bold yellow",
        "code.keyword": "bold red",
        "code.string": "bold green",
        "code.number": "bold yellow",
    }
)

console = Console(theme=custom_theme)


class AuditFormatter:
    COLOR_GREEN = "\033[92m"
    COLOR_RED = "\033[91m"
    COLOR_YELLOW = "\033[93m"
    COLOR_WHITE = "\033[97m"
    COLOR_RESET = "\033[0m"
    COLOR_BOLD = "\033[1m"
    COLOR_DIM = "\033[2m"

    @classmethod
    def print_banner(cls) -> None:
        ascii_art = r"""
███████╗███████╗██████╗██╗   ██╗██████╗ ███████╗
██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝
███████╗█████╗  ██║     ██║   ██║██████╔╝█████╗  
╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝  
███████║███████╗╚██████╗╚██████╔╝██║  ██║███████╗
╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝"""

        banner = f"""{cls.COLOR_GREEN}{cls.COLOR_BOLD}{ascii_art}
{cls.COLOR_YELLOW}  MESIN AUDIT KEAMANAN KODE & ANALISIS FORENSIK AUTOMATIS v2.0
{cls.COLOR_DIM}  Pengembang: fiqq.rahman | Standar: OWASP Top 10, OWASP ASVS v5.0, CheatSheet Series{cls.COLOR_RESET}
"""
        print(banner)

    @classmethod
    def print_section(cls, title: str, content: str) -> None:
        print(f"\n{cls.COLOR_GREEN}{'=' * 80}{cls.COLOR_RESET}")
        print(
            f"{cls.COLOR_BOLD}{cls.COLOR_YELLOW}[ REPORT ] » {title.upper()}{cls.COLOR_RESET}"
        )
        print(f"{cls.COLOR_GREEN}{'=' * 80}{cls.COLOR_RESET}\n")

        # Render Markdown menggunakan tema khusus (Merah, Hijau, Kuning, Putih)
        md = Markdown(content)
        console.print(md)

        print(f"\n{cls.COLOR_GREEN}{'=' * 80}{cls.COLOR_RESET}\n")

    @classmethod
    def print_error(cls, message: str) -> None:
        console.print(
            f"[bold red][ERROR][/bold red] [bold white]{message}[/bold white]",
            highlight=False,
        )

    @classmethod
    def print_info(cls, message: str) -> None:
        console.print(
            f"[bold yellow][INFO][/bold yellow] [bold white]{message}[/bold white]",
            highlight=False,
        )
