import re
from pathlib import Path


class OWASPParser:
    DEFAULT_OWASP_PATH = r"C:\LOC MY FILE\Project Code\Standar Operating Procedure Secure Code\CheatSheetSeries"

    TARGET_CHEATSHEETS = [
        "Access_Control_Cheat_Sheet.md",
        "Authentication_Cheat_Sheet.md",
        "Authorization_Cheat_Sheet.md",
        "Session_Management_Cheat_Sheet.md",
        "Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.md",
        "SQL_Injection_Prevention_Cheat_Sheet.md",
        "Query_Parameterization_Cheat_Sheet.md",
        "OS_Command_Injection_Defense_Cheat_Sheet.md",
        "LDAP_Injection_Prevention_Cheat_Sheet.md",
        "XML_External_Entity_Prevention_Cheat_Sheet.md",
        "Input_Validation_Cheat_Sheet.md",
        "File_Upload_Cheat_Sheet.md",
        "Cross_Site_Scripting_Prevention_Cheat_Sheet.md",
        "DOM_based_XSS_Prevention_Cheat_Sheet.md",
        "XSS_Filter_Evasion_Cheat_Sheet.md",
        "Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.md",
        "Content_Security_Policy_Cheat_Sheet.md",
        "DOM_Clobbering_Prevention_Cheat_Sheet.md",
        "Clickjacking_Defense_Cheat_Sheet.md",
        "HTML5_Security_Cheat_Sheet.md",
        "Securing_Cascading_Style_Sheets_Cheat_Sheet.md",
        "Third_Party_Javascript_Management_Cheat_Sheet.md",
        "Prototype_Pollution_Prevention_Cheat_Sheet.md",
        "XS_Leaks_Cheat_Sheet.md",
        "REST_Security_Cheat_Sheet.md",
        "GraphQL_Cheat_Sheet.md",
        "JSON_Web_Token_Cheat_Sheet.md",
        "HTTP_Headers_Cheat_Sheet.md",
        "HTTP_Strict_Transport_Security_Cheat_Sheet.md",
        "Server_Side_Request_Forgery_Prevention_Cheat_Sheet.md",
        "Unvalidated_Redirects_and_Forwards_Cheat_Sheet.md",
        "AJAX_Security_Cheat_Sheet.md",
        "Laravel_Cheat_Sheet.md",
        "PHP_Configuration_Cheat_Sheet.md",
        "Mass_Assignment_Cheat_Sheet.md",
        "Password_Storage_Cheat_Sheet.md",
        "Forgot_Password_Cheat_Sheet.md",
        "Denial_of_Service_Cheat_Sheet.md",
        "Logging_Cheat_Sheet.md",
    ]

    def __init__(self, owasp_repo_path: str | None = None):
        target_path = owasp_repo_path or self.DEFAULT_OWASP_PATH
        self.base_dir = Path(target_path).resolve()
        self.index_file = self.base_dir / "Index.md"
        self.cheatsheet_dir = self.base_dir / "cheatsheets"

    def _extract_target_files_from_index(self) -> list[Path]:
        if not self.index_file.exists():
            raise FileNotFoundError(
                f"File Index.md tidak ditemukan di: {self.index_file}"
            )

        index_content = self.index_file.read_text(encoding="utf-8")
        matches = re.findall(r"\]\((cheatsheets/.*?\.md)\)", index_content)

        selected_files: list[Path] = []
        for relative_path in matches:
            filename = Path(relative_path).name
            if filename in self.TARGET_CHEATSHEETS:
                full_path = self.base_dir / relative_path
                if full_path.exists() and full_path not in selected_files:
                    selected_files.append(full_path)

        return selected_files

    def load_knowledge_context(self, max_chars_per_file: int = 2500) -> str:
        target_files = self._extract_target_files_from_index()

        if not target_files:
            raise RuntimeError(
                "Tidak ada file cheatsheet yang cocok ditemukan dari Index.md!"
            )

        knowledge_base: list[str] = []

        for file_path in target_files:
            content = file_path.read_text(encoding="utf-8")
            truncated_content = content[:max_chars_per_file]
            knowledge_base.append(
                f"=== OWASP RULE: {file_path.name} ===\n{truncated_content}\n"
            )

        return "\n".join(knowledge_base)
