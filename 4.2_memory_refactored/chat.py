from api import call_zhipu_api
from roles import get_role_prompt, get_break_rules

def chat_once(history, user_input, system_message=None):
    """进行一次对话交互，返回AI的回复内容"""
    # 先把用户消息加入历史
    history.append({"role": "user", "content": user_input})
    
    # 构造API消息列表
    # 如果提供了 system_message，使用它；否则从 history 中找第一个 system 消息
    if system_message:
        api_messages = [{"role": "system", "content": system_message}] + history[1:]
    else:
        # 如果没有提供 system_message，使用 history 中的第一个 system 消息（如果存在）
        api_messages = history if history and history[0].get("role") == "system" else history
    
    result = call_zhipu_api(api_messages)
    assistant_reply = result["choices"][0]["message"]["content"]
    
    # 将AI回复也加入历史
    history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply