import json
from pathlib import Path


class OWASPASVSParser:
    DEFAULT_ASVS_PATH = r"C:\LOC MY FILE\Project Code\Standar Operating Procedure Secure Code\OWASP_Application_Security_Verification_Standard_5.0.0_en.json"

    def __init__(self, asvs_file_path: str | None = None):
        target_path = asvs_file_path or self.DEFAULT_ASVS_PATH
        self.asvs_file = Path(target_path).resolve()

    def _read_json_payload(self) -> dict:
        if not self.asvs_file.exists():
            raise FileNotFoundError(
                f"File ASVS JSON tidak ditemukan di: {self.asvs_file}"
            )

        try:
            with open(self.asvs_file, mode="r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as err:
            raise ValueError(f"Gagal melakukan parsing file ASVS JSON: {str(err)}")

    def _extract_requirements_from_node(
        self, node: list | dict, output_list: list[str]
    ) -> None:
        if isinstance(node, dict):
            req_id = node.get("Shortcode") or node.get("Item") or node.get("Ordinal")
            req_desc = node.get("Description") or node.get("Name")

            if req_id and req_desc:
                output_list.append(f"[{req_id}] {req_desc.strip()}")

            for value in node.values():
                if isinstance(value, (dict, list)):
                    self._extract_requirements_from_node(value, output_list)

        elif isinstance(node, list):
            for item in node:
                self._extract_requirements_from_node(item, output_list)

    def load_asvs_knowledge_base(self, max_chars_total: int = 15000) -> str:
        payload = self._read_json_payload()
        extracted_rules: list[str] = []

        self._extract_requirements_from_node(payload, extracted_rules)

        if not extracted_rules:
            raw_text = json.dumps(payload, ensure_ascii=False)
            return f"=== OWASP ASVS v5.0.0 ===\n{raw_text[:max_chars_total]}"

        formatted_knowledge = "\n".join([f"- {rule}" for rule in extracted_rules])
        truncated_content = formatted_knowledge[:max_chars_total]

        return f"=== OWASP ASVS v5.0.0 (Parsed Verification Rules) ===\n{truncated_content}\n"
