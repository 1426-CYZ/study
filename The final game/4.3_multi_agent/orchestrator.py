from agent import think, advise
from api import call_api
from config import ROLES


def process(user_question: str) -> dict:
    return process_with_context(user_question, [])


def process_with_context(user_question: str, discussion_context: list) -> dict:
    context_summary = ""
    if discussion_context:
        context_summary = "\n\n之前的讨论内容：\n"
        for idx, ctx in enumerate(discussion_context, 1):
            context_summary += f"\n[讨论 {idx}] 问题：{ctx['question']}\n"
            for role in ROLES:
                if role in ctx['answers']:
                    context_summary += f"{role}的回答：{ctx['answers'][role]}\n"
        context_summary += "\n当前问题是在之前讨论基础上的延伸：\n"

    enhanced_question = user_question
    if context_summary:
        enhanced_question = context_summary + user_question

    print("\n[步骤1] 四个角色正在思考...")
    initial_answers = {}
    for role in ROLES:
        print(f"  {role}正在思考...")
        initial_answers[role] = think(role, enhanced_question)
        print(f"  {role}初步回答：{initial_answers[role]}\n")

    print("[步骤2] 角色之间互相给建议...")
    all_advices = {}
    for i, role in enumerate(ROLES):
        other_role = ROLES[(i + 1) % len(ROLES)]
        print(f"  {role}正在给{other_role}建议...")
        advice = advise(role, enhanced_question, initial_answers[other_role], other_role)
        if other_role not in all_advices:
            all_advices[other_role] = []
        all_advices[other_role].append(f"{role}的建议：{advice}")
        print(f"  {role}给{other_role}的建议：{advice}\n")

    print("[步骤3] 整合所有角色的回答和建议...")
    advice_summary = "\n\n".join([f"{role}收到的建议：\n" + "\n".join(all_advices.get(role, [])) for role in ROLES])

    messages = [
        {"role": "system", "content": "你是一个整合者，负责将多个角色的回答和建议整合成一个完整的回答。"},
        {"role": "user", "content": f"""用户问题：{user_question}
{context_summary if context_summary else ""}
各角色的初步回答：
{chr(10).join([f"{role}：{initial_answers[role]}" for role in ROLES])}

{advice_summary}

请整合以上所有角色的回答和建议，生成一个完整、连贯的最终回答。直接给出最终回答，不要其他说明。"""}
    ]

    final_answer = call_api(messages)

    return {
        "question": user_question,
        "initial_answers": initial_answers,
        "advices": all_advices,
        "final_answer": final_answer
    }
