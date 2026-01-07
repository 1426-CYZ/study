def should_exit_by_user(user_input: str) -> bool:
    exit_phrases = [
        "再见", "退出", "结束", "bye", "exit", "quit",
        "不聊了", "别聊了", "不说了", "别说了",
        "不想聊了", "不想继续了", "别聊下去了", "不聊下去了",
        "结束对话", "停止对话", "终止对话"
    ]
    user_input_lower = user_input.strip().lower()
    for phrase in exit_phrases:
        if phrase in user_input_lower:
            return True
    return False

