import os
import time
from google import genai
from google.genai import types

from config.settings import GEMINI_MODEL_NAME, AUDIT_TEMPERATURE
from knowledge.owasp_parser import OWASPParser
from knowledge.top10_parser import OWASPTop10Parser
from knowledge.asps_parser import OWASPASVSParser
from core.rule_parser import CustomRuleParser

# Gunakan murni seri Gemini 3.x aktif
FALLBACK_MODELS = [
    GEMINI_MODEL_NAME,  # gemini-3.6-flash
    "gemini-3.1-flash-lite",  # Fallback 1: Ringan & kencang
    "gemini-3.1-pro-preview",  # Fallback 2: Reasoning tinggi
    "gemini-3-flash-preview",  # Fallback 3: Preview alternatif
]


class CodeAuditor:
    def __init__(self, api_key: str | None = None, custom_rule_path: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API Key Gemini tidak ditemukan! Setel GEMINI_API_KEY pada file .env"
            )

        self.client = genai.Client(api_key=self.api_key)

        self.cs_parser = OWASPParser()
        self.top10_parser = OWASPTop10Parser()
        self.asvs_parser = OWASPASVSParser()
        self.custom_parser = CustomRuleParser(rule_file_path=custom_rule_path)

    def _build_aggregated_knowledge(self) -> str:
        knowledge_blocks: list[str] = []

        try:
            cs_kb = self.cs_parser.load_knowledge_context(max_chars_per_file=1500)
            knowledge_blocks.append(cs_kb)
        except Exception as err:
            knowledge_blocks.append(f"[WARN] Failed loading CheatSheets: {err}")

        try:
            top10_kb = self.top10_parser.load_pdf_knowledge_base(
                max_chars_per_file=2000
            )
            knowledge_blocks.append(top10_kb)
        except Exception as err:
            knowledge_blocks.append(f"[WARN] Failed loading Top10 PDFs: {err}")

        try:
            asvs_kb = self.asvs_parser.load_asvs_knowledge_base(max_chars_total=8000)
            knowledge_blocks.append(asvs_kb)
        except Exception as err:
            knowledge_blocks.append(f"[WARN] Failed loading ASVS JSON: {err}")

        try:
            custom_kb = self.custom_parser.load_custom_rules()
            knowledge_blocks.append(custom_kb)
        except Exception as err:
            knowledge_blocks.append(f"[WARN] Failed loading Custom Rules: {err}")

        return "\n\n".join(knowledge_blocks)

    def _execute_with_fallback(self, system_instruction: str, prompt: str) -> str:
        last_exception = None

        for model_name in FALLBACK_MODELS:
            max_retries = 3
            backoff_delay = 2

            for attempt in range(1, max_retries + 1):
                try:
                    chat = self.client.chats.create(
                        model=model_name,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=AUDIT_TEMPERATURE,
                        ),
                    )
                    response = chat.send_message(prompt)
                    if response.text:
                        return response.text
                except Exception as err:
                    last_exception = err
                    err_msg = str(err)

                    # Langsung loncat ke model berikutnya jika 404 (Model tidak ada)
                    if "404" in err_msg or "NOT_FOUND" in err_msg:
                        break

                    # Retry jika server sibuk / rate-limited (503 / 429)
                    if "503" in err_msg or "UNAVAILABLE" in err_msg or "429" in err_msg:
                        if attempt < max_retries:
                            time.sleep(backoff_delay)
                            backoff_delay *= 2
                            continue

            continue

        raise RuntimeError(
            f"Seluruh model Gemini sibuk/gagal setelah retry. Error terakhir: {str(last_exception)}"
        )

    def audit_source_code(self, source_code: str, file_name: str = "snippet.py") -> str:
        knowledge_context = self._build_aggregated_knowledge()

        system_instruction = (
            "Ente adalah Senior Cybersecurity Auditor dan Principal Software Engineer. "
            "Tugas ente adalah melakukan security code review secara ketat berdasarkan "
            "OWASP CheatSheet Series, OWASP Top 10, OWASP ASVS v5.0.0, dan Aturan Internal.\n\n"
            "Gunakan referensi Knowledge Base berikut sebagai standar audit utama:\n"
            f"{knowledge_context}\n\n"
            "Format Laporan Audit harus mencakup:\n"
            "1. Ringkasan Kerentanan (Temuan, Severity Level, Dampak)\n"
            "2. Analisis Forensik Baris Kode (Baris bermasalah & penyebab teknis)\n"
            "3. Pelanggaran Standar OWASP / ASVS / Internal SOP\n"
            "4. Refactoring Kode Aman (Tulis kode perbaikan tanpa komentar berlebih, modular, & aman)\n"
            "5. Mitigasi tambahan / Rekomendasi Arsitektur"
        )

        prompt = f"Lakukan audit keamanan pada berkas `{file_name}` berikut:\n\n```\n{source_code}\n```"

        return self._execute_with_fallback(system_instruction, prompt)
