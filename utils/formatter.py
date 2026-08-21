import sys


class AuditFormatter:
    # ANSI Color Codes
    COLOR_HEADER = "\033[95m"
    COLOR_BLUE = "\033[94m"
    COLOR_GREEN = "\033[92m"
    COLOR_YELLOW = "\033[93m"
    COLOR_RED = "\033[91m"
    COLOR_RESET = "\033[0m"
    COLOR_BOLD = "\033[1m"

    @classmethod
    def print_banner(cls) -> None:
        banner = f"""
{cls.COLOR_RED}{cls.COLOR_BOLD}
   ____   ____ _  _______  ____  ____    _  ___   _______  ____ _____ 
  / __ \ / __/| |/ /  _  |/ __ \/ __ \  / |/ / | / /  _  |/ __ \___ / 
 / /_/ /_\ \  |   // /_| / /_/ / /_/ / /    /  |/ / /_| / /_/ /|_ \ 
 \____/____/  |_|\_\_/ |_| .___/ .___/ /_/|_/|___/\_/ |_| .___/____/ 
                         /_/   /_/                      /_/           
{cls.COLOR_BLUE}========== AUTOMATED SECURITY CODE REVIEW ENGINE v1.0 ==========
{cls.COLOR_RESET}"""
        print(banner)

    @classmethod
    def print_section(cls, title: str, content: str) -> None:
        border = "=" * 80
        print(f"\n{cls.COLOR_YELLOW}{border}{cls.COLOR_RESET}")
        print(
            f"{cls.COLOR_GREEN}{cls.COLOR_BOLD}[ AUDIT REPORT ] {title}{cls.COLOR_RESET}"
        )
        print(f"{cls.COLOR_YELLOW}{border}{cls.COLOR_RESET}\n")
        print(content)
        print(f"\n{cls.COLOR_YELLOW}{border}{cls.COLOR_RESET}\n")

    @classmethod
    def print_error(cls, message: str) -> None:
        print(
            f"{cls.COLOR_RED}{cls.COLOR_BOLD}[ERROR] {message}{cls.COLOR_RESET}",
            file=sys.stderr,
        )

    @classmethod
    def print_info(cls, message: str) -> None:
        print(f"{cls.COLOR_BLUE}{cls.COLOR_BOLD}[INFO] {message}{cls.COLOR_RESET}")
