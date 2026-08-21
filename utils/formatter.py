import sys
import textwrap


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
    def _format_content(cls, raw_content: str, width: int = 80) -> str:
        formatted_lines = []
        lines = raw_content.splitlines()

        for line in lines:
            wrapped = textwrap.fill(line, width=width) if len(line) > width else line

            upper_line = wrapped.upper()
            if any(
                k in upper_line
                for k in [
                    "CRITICAL",
                    "HIGH",
                    "KERENTANAN",
                    "BAHAYA",
                    "VULNERABILITY",
                    "ERROR",
                ]
            ):
                formatted_lines.append(
                    f"{cls.COLOR_RED}{cls.COLOR_BOLD}{wrapped}{cls.COLOR_RESET}"
                )
            elif any(
                k in upper_line
                for k in [
                    "LOW",
                    "SAFE",
                    "AMAN",
                    "REKOMENDASI",
                    "REFACTORED",
                    "FIXED",
                ]
            ):
                formatted_lines.append(
                    f"{cls.COLOR_GREEN}{cls.COLOR_BOLD}{wrapped}{cls.COLOR_RESET}"
                )
            else:
                formatted_lines.append(f"{cls.COLOR_WHITE}{wrapped}{cls.COLOR_RESET}")

        return "\n".join(formatted_lines)

    @classmethod
    def print_section(cls, title: str, content: str) -> None:
        border = "=" * 80
        print(f"\n{cls.COLOR_GREEN}{border}{cls.COLOR_RESET}")
        print(
            f"{cls.COLOR_BOLD}{cls.COLOR_WHITE}[ REPORT ] » {title.upper()}{cls.COLOR_RESET}"
        )
        print(f"{cls.COLOR_GREEN}{border}{cls.COLOR_RESET}\n")
        print(cls._format_content(content))
        print(f"\n{cls.COLOR_GREEN}{border}{cls.COLOR_RESET}\n")

    @classmethod
    def print_error(cls, message: str) -> None:
        print(
            f"{cls.COLOR_RED}{cls.COLOR_BOLD}[ERROR] {message}{cls.COLOR_RESET}",
            file=sys.stderr,
        )

    @classmethod
    def print_info(cls, message: str) -> None:
        print(f"{cls.COLOR_CYAN}{cls.COLOR_BOLD}[INFO] {message}{cls.COLOR_RESET}")
