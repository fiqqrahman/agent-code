import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Target Default Paths
OWASP_CHEATSHEET_PATH = os.getenv(
    "OWASP_CHEATSHEET_PATH",
    r"C:\LOC MY FILE\Project Code\Standar Operating Procedure Secure Code\CheatSheetSeries",
)
OWASP_TOP10_PDF_PATH = os.getenv(
    "OWASP_TOP10_PDF_PATH",
    r"C:\LOC MY FILE\Project Code\Standar Operating Procedure Secure Code\Top10 Vuln",
)
OWASP_ASVS_JSON_PATH = os.getenv(
    "OWASP_ASVS_JSON_PATH",
    r"C:\LOC MY FILE\Project Code\Standar Operating Procedure Secure Code\OWASP_Application_Security_Verification_Standard_5.0.0_en.json",
)

# LLM Configuration (Set ke Seri 3 Resmi)
GEMINI_MODEL_NAME = "gemini-3.6-flash"
AUDIT_TEMPERATURE = 0.2

# Supported Extensions for Git Diff Audit
SUPPORTED_EXTENSIONS = {".php", ".py", ".js", ".ts", ".go", ".java", ".c", ".cpp"}
