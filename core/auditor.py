import os
import time
from google import genai
from google.genai import types

from config.settings import GEMINI_MODEL_NAME, AUDIT_TEMPERATURE
from knowledge.owasp_parser import OWASPParser
from knowledge.top10_parser import OWASPTop10Parser
from knowledge.asps_parser import OWASPASVSParser
from core.rule_parser import CustomRuleParser

FALLBACK_MODELS = [
    GEMINI_MODEL_NAME,  # gemini-3.6-flash
    "gemini-3.1-flash-lite",
    "gemini-3.1-pro-preview",
    "gemini-3-flash-preview",
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

    def load_and_verify_knowledge_base(self, logger_func=None) -> str:
        knowledge_blocks: list[str] = []

        if logger_func:
            logger_func(
                "Memeriksa & memuat berkas panduan keamanan (Knowledge Base)..."
            )

        # 1. OWASP CheatSheet Series
        try:
            cs_kb = self.cs_parser.load_knowledge_context(max_chars_per_file=1500)
            knowledge_blocks.append(cs_kb)
            if logger_func:
                logger_func(
                    "Pemuatan OWASP CheatSheet Series ................. [ DONE ]"
                )
        except Exception as err:
            if logger_func:
                logger_func(
                    f"Pemuatan OWASP CheatSheet Series ................. [ FAILED: {err} ]"
                )

        # 2. OWASP Top 10 PDF
        try:
            top10_kb = self.top10_parser.load_pdf_knowledge_base(
                max_chars_per_file=2000
            )
            knowledge_blocks.append(top10_kb)
            if logger_func:
                logger_func(
                    "Pemuatan OWASP Top 10 Document ................... [ DONE ]"
                )
        except Exception as err:
            if logger_func:
                logger_func(
                    f"Pemuatan OWASP Top 10 Document ................... [ FAILED: {err} ]"
                )

        # 3. OWASP ASVS v5.0.0 JSON
        try:
            asvs_kb = self.asvs_parser.load_asvs_knowledge_base(max_chars_total=8000)
            knowledge_blocks.append(asvs_kb)
            if logger_func:
                logger_func(
                    "Pemuatan OWASP ASVS v5.0.0 Specification ........ [ DONE ]"
                )
        except Exception as err:
            if logger_func:
                logger_func(
                    f"Pemuatan OWASP ASVS v5.0.0 Specification ........ [ FAILED: {err} ]"
                )

        # 4. Custom Internal SOP Rules
        try:
            custom_kb = self.custom_parser.load_custom_rules()
            knowledge_blocks.append(custom_kb)
            if logger_func:
                logger_func(
                    "Pemuatan SOP Rules & Internal Security Policy .... [ DONE ]"
                )
        except Exception as err:
            if logger_func:
                logger_func(
                    f"Pemuatan SOP Rules & Internal Security Policy .... [ FAILED: {err} ]"
                )

        if logger_func:
            logger_func(
                "Seluruh sumber pedoman keamanan berhasil dimuat secara optimal.\n"
            )

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

                    if "404" in err_msg or "NOT_FOUND" in err_msg:
                        break

                    if "503" in err_msg or "UNAVAILABLE" in err_msg or "429" in err_msg:
                        if attempt < max_retries:
                            time.sleep(backoff_delay)
                            backoff_delay *= 2
                            continue

            continue

        raise RuntimeError(
            f"Seluruh model Gemini sibuk/gagal setelah retry. Error terakhir: {str(last_exception)}"
        )

    def audit_source_code(
        self,
        source_code: str,
        file_name: str = "snippet.py",
        knowledge_context: str = "",
    ) -> str:
        system_instruction = (
            "Ente adalah Senior Cybersecurity Auditor dan Principal Software Engineer. "
            "Tugas ente adalah melakukan security code review secara terperinci, mendalam, dan komprehensif "
            "berdasarkan OWASP CheatSheet Series, OWASP Top 10, OWASP ASVS v5.0.0, dan Aturan SOP Internal.\n\n"
            "Gunakan referensi Knowledge Base berikut sebagai standar audit utama:\n"
            f"{knowledge_context}\n\n"
            "Format Laporan Audit Wajib Terstruktur Terperinci:\n"
            "1. Ringkasan Kerentanan (Sajikan tabel komprehensif berisi No, Temuan/Komponen, Severity Level, dan Dampak Keamanan terperinci)\n"
            "2. Analisis Forensik Baris Kode (Uraikan satu per satu setiap temuan secara detail, sertakan nomor baris, penyebab teknis, dan vektor serangan)\n"
            "3. Pelanggaran Standar OWASP / ASVS / SOP Internal (Sebutkan pasal/kategori OWASP Top 10 / ASVS yang dilanggar secara eksplisit)\n"
            "4. Refactoring Kode Aman (Tuliskan perbaikan kode utuh secara modular, aman, dan efisien tanpa komentar berlebih)\n"
            "5. Mitigasi Tambahan / Rekomendasi Arsitektur (Berikan panduan langkah hardened secara terstruktur)"
        )

        prompt = f"Lakukan audit keamanan pada berkas `{file_name}` berikut:\n\n```\n{source_code}\n```"

        return self._execute_with_fallback(system_instruction, prompt)
