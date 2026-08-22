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
            return []
        pdf_entries: list[tuple[int, Path]] = []
        for file_path in self.base_dir.glob("*.pdf"):
            match = re.search(r"(\d{4})", file_path.name)
            year = int(match.group(1)) if match else 2021
            pdf_entries.append((year, file_path))
        return sorted(pdf_entries, key=lambda x: x[0])

    def load_pdf_knowledge_base_with_stats(
        self, max_chars_per_file: int = 3000
    ) -> tuple[str, dict]:
        pdf_files = self._discover_pdf_files()
        stats = {
            "target_total": len(pdf_files),
            "success_count": 0,
            "failed_count": 0,
            "failed_details": [],
        }

        if not self.base_dir.exists():
            stats["failed_details"].append(
                ("Top10 Vuln Path", f"Folder tidak ditemukan di {self.base_dir}")
            )
            return "", stats

        if not pdf_files:
            stats["failed_details"].append(
                (
                    "Top10 Vuln Path",
                    f"Tidak ada berkas PDF ditemukan di {self.base_dir}",
                )
            )
            return "", stats

        knowledge_base: list[str] = []

        for year, pdf_path in pdf_files:
            try:
                reader = PdfReader(pdf_path)
                raw_text = ""
                for page in reader.pages[:5]:
                    extracted = page.extract_text()
                    if extracted:
                        raw_text += extracted + "\n"

                if raw_text.strip():
                    truncated_content = raw_text[:max_chars_per_file]
                    knowledge_base.append(
                        f"=== OWASP TOP 10 YEAR {year} ({pdf_path.name}) ===\n"
                        f"{truncated_content}\n"
                    )
                    stats["success_count"] += 1
                else:
                    stats["failed_count"] += 1
                    stats["failed_details"].append(
                        (pdf_path.name, "Konten teks PDF kosong/tidak terkonversi")
                    )
            except Exception as err:
                stats["failed_count"] += 1
                stats["failed_details"].append(
                    (pdf_path.name, f"Eror membaca PDF: {str(err)}")
                )

        return "\n".join(knowledge_base), stats
