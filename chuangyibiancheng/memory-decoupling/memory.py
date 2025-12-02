import json
import os
from typing import Any, Dict, List


def load_memory(file_path: str) -> List[Dict[str, Any]]:
    """从 JSON 文件加载对话历史，返回对话历史列表。"""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            history = data.get("history", [])
            print(f"✓ 已加载 {len(history)} 条历史对话")
            return history
        except Exception as e:
            print(f"⚠ 加载记忆失败: {e}，将使用新的对话历史")
            return []
    else:
        print("✓ 未找到记忆文件，开始新对话")
        return []


def save_memory(file_path: str, role_system: str, conversation_history: List[Dict[str, Any]]) -> None:
    """保存对话历史到 JSON 文件。"""
    from datetime import datetime

    try:
        data: Dict[str, Any] = {
            "role_system": role_system,
            "history": conversation_history,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ 已保存 {len(conversation_history)} 条对话到记忆文件")
    except Exception as e:
        print(f"⚠ 保存记忆失败: {e}")


