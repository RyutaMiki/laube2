import json
from pathlib import Path

class ErrorMessageLoader:
    def __init__(self, filepath="app/constants/error_messages.json"):
        self.messages = json.loads(Path(filepath).read_text(encoding="utf-8"))

    def get_message(self, code: str) -> str:
        return self.messages.get(code, f"[{code}] 不明なエラーコードです")