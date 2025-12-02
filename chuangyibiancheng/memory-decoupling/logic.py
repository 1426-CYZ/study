def should_exit_by_user(user_input: str) -> bool:
    """判断用户是否想要结束对话。"""
    return user_input.strip() in ["再见", "结束"]


def should_exit_by_ai(ai_reply: str) -> bool:
    """判断 AI 的回复是否表示要结束对话。"""
    reply_cleaned = (
        ai_reply.strip()
        .replace(" ", "")
        .replace("！", "")
        .replace("!", "")
        .replace("，", "")
        .replace(",", "")
    )
    return reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned)


