from .config import ROLES
from .agent import think, advise, judge_survival_status, generate_followup_suggestions
from .memory_store import save_role_memories


def process_with_context(
    user_question: str,
    discussion_context: list,
    input_listener=None,
    preset_summary: str = "",
):
    context_summary = ""
    if discussion_context:
        context_summary = "\n\n之前的讨论内容：\n"
        for idx, ctx in enumerate(discussion_context, 1):
            context_summary += f"\n[讨论 {idx}] 问题：{ctx['question']}\n"
            for role in ROLES:
                if role in ctx.get("answers", {}):
                    context_summary += f"{role}的回答：{ctx['answers'][role]}\n"
        context_summary += "\n当前问题是在之前讨论基础上的延伸：\n"

    preset_prefix = f"【场景预设】\n{preset_summary}\n\n" if preset_summary else ""
    enhanced_question = preset_prefix + (context_summary + user_question if context_summary else user_question)

    print("\n[步骤1] 四个角色正在思考...")
    initial_answers = {}
    for idx, role in enumerate(ROLES):
        print(f"  {role}正在思考...")
        initial_answers[role] = think(role, enhanced_question, preset_summary)
        print(f"  {role}初步回答：{initial_answers[role]}\n")

        if input_listener and idx < len(ROLES) - 1:
            if input_listener.add_check_point(f"[检查点] {role}已回答，是否继续？"):
                user_input = input_listener.get_input()
                if user_input:
                    print(f"\n[用户打断] 收到输入：{user_input}")
                    return {"interrupted": True, "user_input": user_input}

    if input_listener:
        if input_listener.add_check_point("\n[检查点] 所有角色已回答，是否继续到建议阶段？"):
            user_input = input_listener.get_input()
            if user_input:
                print(f"\n[用户打断] 收到输入：{user_input}")
                return {"interrupted": True, "user_input": user_input}

    print("[步骤2] 角色之间互相给建议...")
    all_advices = {}
    for i, role in enumerate(ROLES):
        other_role = ROLES[(i + 1) % len(ROLES)]
        print(f"  {role}正在给{other_role}建议...")
        advice = advise(role, enhanced_question, initial_answers[other_role], other_role, preset_summary)
        all_advices.setdefault(other_role, []).append(f"{role}的建议：{advice}")
        print(f"  {role}给{other_role}的建议：{advice}\n")

        if input_listener and i < len(ROLES) - 1:
            if input_listener.add_check_point(f"[检查点] {role}已给出建议，是否继续？"):
                user_input = input_listener.get_input()
                if user_input:
                    print(f"\n[用户打断] 收到输入：{user_input}")
                    return {"interrupted": True, "user_input": user_input}

    if input_listener:
        if input_listener.add_check_point("\n[检查点] 所有建议已完成，是否继续整合？"):
            user_input = input_listener.get_input()
            if user_input:
                print(f"\n[用户打断] 收到输入：{user_input}")
                return {"interrupted": True, "user_input": user_input}

    print("[步骤3] 整合所有角色的回答和建议...")
    advice_summary = "\n\n".join(
        [f"{role}收到的建议：\n" + "\n".join(all_advices.get(role, [])) for role in ROLES]
    )

    messages = [
        {"role": "system", "content": "你是一个整合者，负责将多个角色的回答和建议整合成一个完整的回答。"},
        {
            "role": "user",
            "content": (
                f"【场景预设】\n{preset_summary}\n\n"
                f"用户问题：{user_question}\n"
                f"{context_summary if context_summary else ''}"
                "各角色的初步回答：\n"
                f"{chr(10).join([f'{role}：{initial_answers[role]}' for role in ROLES])}\n\n"
                f"{advice_summary}\n\n"
                "请整合以上所有角色的回答和建议，生成一个完整、连贯的最终回答。直接给出最终回答，不要其他说明。"
            ),
        },
    ]

    from .api import call_api  # local import to avoid cycle

    final_answer = call_api(messages)

    print("[步骤4] 判断用户生存状态...")
    survival_status = judge_survival_status(user_question, final_answer, discussion_context, preset_summary)

    result = {
        "question": user_question,
        "initial_answers": initial_answers,
        "advices": all_advices,
        "final_answer": final_answer,
        "survival_status": survival_status,
        "interrupted": False,
    }

    save_role_memories(result, preset_summary, discussion_context)
    followup_options = generate_followup_suggestions(
        preset_summary, user_question, final_answer, discussion_context, limit=3
    )
    result["followup_options"] = followup_options
    return result

