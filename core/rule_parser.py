import json
from pathlib import Path


class CustomRuleParser:
    def __init__(self, rule_file_path: str | Path | None = None):
        self.rule_file = Path(rule_file_path).resolve() if rule_file_path else None

    def load_custom_rules(self) -> str:
        if not self.rule_file or not self.rule_file.exists():
            return "[INFO] No custom rules applied."

        try:
            with open(self.rule_file, mode="r", encoding="utf-8") as file:
                data = json.load(file)
                rules = data.get("rules", [])
                formatted_rules = "\n".join(
                    [
                        f"- [{r.get('id', 'CUSTOM')}] {r.get('description', '')}"
                        for r in rules
                    ]
                )
                return f"=== ATURAN KEAMANAN INTERNAL/SOP ===\n{formatted_rules}\n"
        except Exception as err:
            return f"[WARN] Failed loading custom rules: {str(err)}"
