import os
import json
import datetime
from .config import ROLES, DISCUSSION_MEMORY_FILE


def save_role_memories(result: dict, preset_summary: str, discussion_context: list):
    try:
        os.makedirs(os.path.dirname(DISCUSSION_MEMORY_FILE), exist_ok=True)
        context_index = len(discussion_context) + 1
        timestamp = datetime.datetime.now().isoformat()
        with open(DISCUSSION_MEMORY_FILE, "a", encoding="utf-8") as f:
            for role in ROLES:
                entry = {
                    "timestamp": timestamp,
                    "context_index": context_index,
                    "role": role,
                    "question": result.get("question", ""),
                    "answer": result.get("initial_answers", {}).get(role, ""),
                    "advices_to_role": result.get("advices", {}).get(role, []),
                    "final_answer": result.get("final_answer", ""),
                    "preset_summary": preset_summary,
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[警告] 保存讨论记忆失败：{e}")

