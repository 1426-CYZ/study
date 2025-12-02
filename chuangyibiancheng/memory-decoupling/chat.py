from typing import List, Dict, Any

from .api import call_zhipu_api


def chat_once(history: List[Dict[str, Any]], system_message: str, user_input: str) -> str:
    """进行一次对话交互，返回 AI 的回复内容。"""
    # 先把用户消息加入历史
    history.append({"role": "user", "content": user_input})

    # 重新构造带 system 的消息列表（避免 system 被多次追加）
    api_messages: List[Dict[str, Any]] = [{"role": "system", "content": system_message}] + history[1:]

    result = call_zhipu_api(api_messages)
    assistant_reply = result["choices"][0]["message"]["content"]

    # 将 AI 回复也加入历史
    history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply


