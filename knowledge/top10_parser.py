import re
import logging
from pathlib import Path
from pypdf import PdfReader

logging.getLogger("pypdf").setLevel(logging.ERROR)


class OWASPTop10Parser:
    DEFAULT_PDF_DIR = r"C:\LOC MY FILE\Project Code\Standar Operating Procedure Secure Code\Top10 Vuln"

    def __init__(self, pdf_dir_path: str | None = None):
        target_path = pdf_dir_path or self.DEFAULT_PDF_DIR
        self.base_dir = Path(target_path).resolve()

    def _discover_pdf_files(self) -> list[tuple[int, Path]]:
        if not self.base_dir.exists():
            raise FileNotFoundError(f"Directory not found: {self.base_dir}")
        pdf_entries: list[tuple[int, Path]] = []
        for file_path in self.base_dir.glob("OWASP_*.pdf"):
            match = re.search(r"OWASP_(\d{4})\.pdf$", file_path.name, re.IGNORECASE)
            if match:
                year = int(match.group(1))
                pdf_entries.append((year, file_path))
        return sorted(pdf_entries, key=lambda x: x[0])

    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        extracted_text: list[str] = []
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)
        except Exception as err:
            return f"[ERROR] Failed to read PDF {pdf_path.name}: {str(err)}"
        return "\n".join(extracted_text)

    def _parse_top10_vulnerabilities(self, raw_text: str) -> list[str]:
        pattern = re.compile(
            r"((?:A\d{1,2}(?::\d{4})?|\b[1-9]\b|10)[\s\-\:]+[^\n]+)", re.IGNORECASE
        )
        matches = pattern.findall(raw_text)
        unique_rules: list[str] = []
        for match in matches:
            cleaned_rule = " ".join(match.split())
            if cleaned_rule not in unique_rules:
                unique_rules.append(cleaned_rule)
        return unique_rules

    def load_pdf_knowledge_base(self, max_chars_per_file: int = 3000) -> str:
        pdf_files = self._discover_pdf_files()
        if not pdf_files:
            raise RuntimeError(f"No OWASP PDF files found in {self.base_dir}")
        knowledge_base: list[str] = []
        for year, pdf_path in pdf_files:
            raw_text = self._extract_text_from_pdf(pdf_path)
            parsed_rules = self._parse_top10_vulnerabilities(raw_text)
            if parsed_rules:
                content_summary = "\n".join([f"- {rule}" for rule in parsed_rules])
            else:
                content_summary = raw_text[:max_chars_per_file]
            truncated_content = content_summary[:max_chars_per_file]
            knowledge_base.append(
                f"=== OWASP TOP 10 YEAR {year} ({pdf_path.name}) ===\n"
                f"{truncated_content}\n"
            )
        return "\n".join(knowledge_base)
