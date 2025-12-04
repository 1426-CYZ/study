from datetime import datetime
from memory import load_memory, save_memory
from roles import get_role_prompt, get_break_rules
from logic import should_exit_by_user, should_exit_by_ai
from chat import chat_once

# 全局配置
MEMORY_FILE = "conversation_memory.json"

def main():
    """主程序入口：初始化对话历史，运行主循环，保存记忆"""
    role_name = "盲眼诗人"
    role_system = get_role_prompt(role_name)
    break_message = get_break_rules(role_name)
    system_message = role_system + "\n\n" + break_message
    
    # 加载记忆
    history = load_memory(MEMORY_FILE)
    
    # 如果记忆为空，初始化对话历史
    if not history:
        conversation_history = [{"role": "system", "content": system_message}]
        print("✓ 初始化新对话")
    else:
        # 如果有历史记录，使用历史记录，但确保第一个是 system 消息
        if history and history[0].get("role") == "system":
            conversation_history = history
        else:
            conversation_history = [{"role": "system", "content": system_message}] + history
    
    print("\n对话开始（输入\"再见\"可结束）：")
    
    try:
        while True:
            user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")
            
            # 用户主动结束
            if should_exit_by_user(user_input):
                print("对话结束，记忆已保存")
                break
            
            # 一轮对话
            assistant_reply = chat_once(conversation_history, user_input, system_message)
            print(assistant_reply)
            
            # 每轮都保存记忆
            save_memory(MEMORY_FILE, {
                "role_system": role_system,
                "history": conversation_history
            })
            
            # AI触发结束
            if should_exit_by_ai(assistant_reply):
                print("\n对话结束，记忆已保存")
                break
    
    except KeyboardInterrupt:
        print("\n\n程序被用户中断，正在保存记忆...")
        save_memory(MEMORY_FILE, {
            "role_system": role_system,
            "history": conversation_history
        })
        print("✓ 记忆已保存")
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        print("正在保存记忆...")
        save_memory(MEMORY_FILE, {
            "role_system": role_system,
            "history": conversation_history
        })
        print("✓ 记忆已保存")

if __name__ == "__main__":
    main()