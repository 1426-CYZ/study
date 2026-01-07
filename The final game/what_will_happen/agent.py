from .api import call_api
from .roles import get_role_prompt
from .config import ROLES


def think(role_name: str, user_question: str, preset_summary: str = "") -> str:
    role_prompt = get_role_prompt(role_name)
    messages = [
        {"role": "system", "content": role_prompt},
        {
            "role": "user",
            "content": (
                f"【场景预设】\n{preset_summary}\n\n"
                f"用户问：{user_question}\n\n"
                f"请基于你{role_name}的身份，思考一个初步回答。直接给出回答内容，不要其他说明。"
            ),
        },
    ]
    return call_api(messages)


def advise(role_name: str, user_question: str, other_answer: str, other_role: str, preset_summary: str = "") -> str:
    role_prompt = get_role_prompt(role_name)
    messages = [
        {"role": "system", "content": role_prompt},
        {
            "role": "user",
            "content": (
                f"【场景预设】\n{preset_summary}\n\n"
                f"用户问：{user_question}\n\n"
                f"{other_role}的初步回答：{other_answer}\n\n"
                f"作为{role_name}，请给{other_role}一个建议，告诉他如何改进这个回答。"
                "直接给出建议内容，不要其他说明。"
            ),
        },
    ]
    return call_api(messages)


def judge_survival_status(user_question: str, final_answer: str, discussion_context: list, preset_summary: str = "") -> str:
    context_info = ""
    if discussion_context:
        context_info = "\n\n之前的讨论历史：\n"
        for idx, ctx in enumerate(discussion_context, 1):
            context_info += f"\n[讨论 {idx}] 问题：{ctx['question']}\n"
            if 'answers' in ctx:
                for role in ROLES:
                    if role in ctx['answers']:
                        context_info += f"{role}的回答：{ctx['answers'][role]}\n"

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个生存状态评估专家。基于给定的场景和讨论结果，"
                "你需要判断在这个场景中，用户（'我'）最终是死亡还是存活。"
                "核心场景：如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？"
                "请仔细分析讨论内容，判断用户在这个场景中的最终生存状态。"
                "你只能回答'死亡'或'存活'，不要添加任何其他文字说明。"
            )
        },
        {
            "role": "user",
            "content": (
                f"【场景预设】\n{preset_summary}\n\n"
                f"当前问题：{user_question}\n"
                f"{context_info}\n"
                f"最终讨论结果：{final_answer}\n\n"
                "请基于以上信息，判断在这个场景中，用户（'我'）最终是死亡还是存活？"
                "只回答'死亡'或'存活'，不要添加任何其他文字。"
            ),
        },
    ]

    result = call_api(messages).strip()

    if "死亡" in result or "死" in result:
        return "死亡"
    if "存活" in result or "活" in result or "生存" in result:
        return "存活"
    result_lower = result.lower()
    if any(word in result_lower for word in ["die", "dead", "death", "kill", "死亡", "死"]):
        return "死亡"
    return "存活"


def generate_followup_suggestions(
    preset_summary: str,
    user_question: str,
    final_answer: str,
    discussion_context: list,
    limit: int = 3,
) -> list:
    context_info = ""
    if discussion_context:
        context_info = "\n\n之前的讨论历史：\n"
        for idx, ctx in enumerate(discussion_context, 1):
            context_info += f"\n[讨论 {idx}] 问题：{ctx.get('question','')}\n"
            if 'answers' in ctx:
                for role in ROLES:
                    if role in ctx['answers']:
                        context_info += f"{role}的回答：{ctx['answers'][role]}\n"

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个追问建议生成器。请基于场景预设、当前问题、讨论历史和最终回答，"
                "给出简短、具体、可操作的追问建议。每条建议不超过20个字。输出用换行分隔，每行一条。"
            )
        },
        {
            "role": "user",
            "content": (
                f"【场景预设】\n{preset_summary}\n\n"
                f"当前问题：{user_question}\n"
                f"{context_info}\n"
                f"最终讨论结果：{final_answer}\n\n"
                f"请给出 {limit} 条新的追问建议，用换行分隔。"
            )
        }
    ]

    suggestions_text = call_api(messages)
    lines = [line.strip(" -•\t") for line in suggestions_text.splitlines() if line.strip()]
    return lines[:limit]

