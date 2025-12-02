from datetime import datetime
from typing import List, Dict, Any

from .memory import load_memory, save_memory
from .roles import get_role_prompt, get_break_rules
from .logic import should_exit_by_user, should_exit_by_ai
from .chat import chat_once

# 记忆文件路径（与原 memory_101.1.py 保持一致）
MEMORY_FILE = "conversation_memory.json"


def build_system_message(role_name: str) -> str:
    role_system = get_role_prompt(role_name)
    break_message = get_break_rules(role_name)
    return role_system + "\n\n" + break_message


def init_history(system_message: str) -> List[Dict[str, Any]]:
    """初始化对话历史。这里不自动加载旧 history，只在文件层面管理。"""
    return [{"role": "system", "content": system_message}]


def main(role_name: str = "盲眼诗人") -> None:
    """主程序入口：初始化对话历史，运行主循环，保存记忆。"""
    system_message = build_system_message(role_name)
    conversation_history = init_history(system_message)

    print("\n对话开始（输入“再见”可结束）：")

    try:
        while True:
            user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")

            # 用户主动结束
            if should_exit_by_user(user_input):
                print("对话结束，记忆已保存")
                break

            # 一轮对话
            assistant_reply = chat_once(conversation_history, system_message, user_input)
            print(assistant_reply)

            # 每轮都保存记忆
            save_memory(MEMORY_FILE, get_role_prompt(role_name), conversation_history)

            # AI 触发结束
            if should_exit_by_ai(assistant_reply):
                print("\n对话结束，记忆已保存")
                break

    except KeyboardInterrupt:
        print("\n\n程序被用户中断，正在保存记忆...")
        save_memory(MEMORY_FILE, get_role_prompt(role_name), conversation_history)
        print("✓ 记忆已保存")
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        print("正在保存记忆...")
        save_memory(MEMORY_FILE, get_role_prompt(role_name), conversation_history)
        print("✓ 记忆已保存")


if __name__ == "__main__":
    main()


