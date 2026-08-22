import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

console = Console()


class AuditFormatter:
    COLOR_CYAN = "\033[96m"
    COLOR_GREEN = "\033[92m"
    COLOR_RED = "\033[91m"
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
{cls.COLOR_CYAN}  MESIN AUDIT KEAMANAN KODE & ANALISIS FORENSIK AUTOMATIS v2.0
{cls.COLOR_DIM}  Pengembang: fiqq.rahman | Standar: OWASP Top 10, OWASP ASVS v5.0, CheatSheet Series{cls.COLOR_RESET}
"""
        print(banner)

    @classmethod
    def print_section(cls, title: str, content: str) -> None:
        print(f"\n{cls.COLOR_GREEN}{'=' * 80}{cls.COLOR_RESET}")
        print(
            f"{cls.COLOR_BOLD}{cls.COLOR_WHITE}[ AUDIT REPORT ] » {title.upper()}{cls.COLOR_RESET}"
        )
        print(f"{cls.COLOR_GREEN}{'=' * 80}{cls.COLOR_RESET}\n")

        # Magic: Rich Markdown Renderer otomatis mewarnai sintaksis kode & membuatkan kotak berbingkai!
        md = Markdown(content)
        console.print(md)

        print(f"\n{cls.COLOR_GREEN}{'=' * 80}{cls.COLOR_RESET}\n")

    @classmethod
    def print_error(cls, message: str) -> None:
        console.print(f"[bold red][ERROR][/bold red] {message}", highlight=False)

    @classmethod
    def print_info(cls, message: str) -> None:
        console.print(
            f"[bold bold_cyan][INFO][/bold bold_cyan] {message}", highlight=False
        )
