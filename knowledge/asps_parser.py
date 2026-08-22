import json
from pathlib import Path


class OWASPASVSParser:
    DEFAULT_ASVS_PATH = r"C:\LOC MY FILE\Project Code\Standar Operating Procedure Secure Code\OWASP_Application_Security_Verification_Standard_5.0.0_en.json"

    def __init__(self, asvs_file_path: str | None = None):
        target_path = asvs_file_path or self.DEFAULT_ASVS_PATH
        self.asvs_file = Path(target_path).resolve()

    def load_asvs_knowledge_base_with_stats(
        self, max_chars_total: int = 15000
    ) -> tuple[str, dict[str, str | int]]:
        stats: dict[str, str | int] = {
            "file_name": self.asvs_file.name,
            "status": "FAILED",
            "reason": "",
            "total_rules": 0,
        }

        if not self.asvs_file.exists():
            stats["reason"] = f"Berkas JSON tidak ditemukan di {self.asvs_file}"
            return "", stats

        try:
            with open(self.asvs_file, mode="r", encoding="utf-8") as file:
                payload = json.load(file)

            extracted_rules: list[str] = []

            def _extract(node):
                if isinstance(node, dict):
                    req_id = (
                        node.get("Shortcode") or node.get("Item") or node.get("Ordinal")
                    )
                    req_desc = node.get("Description") or node.get("Name")
                    if req_id and req_desc:
                        extracted_rules.append(f"[{req_id}] {req_desc.strip()}")
                    for val in node.values():
                        if isinstance(val, (dict, list)):
                            _extract(val)
                elif isinstance(node, list):
                    for item in node:
                        _extract(item)

            _extract(payload)

            if extracted_rules:
                formatted_knowledge = "\n".join(
                    [f"- {rule}" for rule in extracted_rules]
                )
                truncated_content = formatted_knowledge[:max_chars_total]
                content = (
                    f"=== OWASP ASVS v5.0.0 (Parsed Rules) ===\n{truncated_content}\n"
                )
                stats["status"] = "SUCCESS"
                stats["total_rules"] = len(extracted_rules)
            else:
                raw_text = json.dumps(payload, ensure_ascii=False)
                content = f"=== OWASP ASVS v5.0.0 ===\n{raw_text[:max_chars_total]}"
                stats["status"] = "SUCCESS"
                stats["total_rules"] = 1

            return content, stats

        except Exception as err:
            stats["reason"] = f"Gagal parsing JSON: {str(err)}"
            return "", stats
