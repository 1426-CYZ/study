from .preset import collect_preset, format_preset
from .ui import show_options, show_extended_options, get_user_question_from_input
from .logic import should_exit_by_user
from .config import QUESTION_MAP
from .input_listener import InputListener
from .orchestrator import process_with_context


def main():
    print("=" * 50)
    print("AI议会 - 四个角色的头脑风暴（解耦版）")
    print("核心场景：如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？")
    print("=" * 50)

    preset = collect_preset()
    preset_summary = format_preset(preset)
    if preset_summary:
        print("当前场景预设：")
        print(preset_summary)
        print("=" * 50)

    while True:
        show_options()
        user_input = input("\n你的选择或问题：").strip()

        if should_exit_by_user(user_input):
            print("再见！")
            break

        if not user_input:
            continue

        user_question = get_user_question_from_input(user_input)
        if not user_question:
            print("无效输入")
            continue

        original_choice = user_input if user_input in QUESTION_MAP else None
        discussion_context = []
        current_question = user_question

        print(f"\n你选择的问题：{current_question}\n")

        input_listener = InputListener()

        while True:
            try:
                result = process_with_context(current_question, discussion_context, input_listener, preset_summary)

                if result.get("interrupted"):
                    user_input = result.get("user_input")
                    if should_exit_by_user(user_input):
                        print("再见！")
                        return

                    if user_input.strip() == "追问":
                        follow_question = input("\n请输入你的追问：").strip()
                        if should_exit_by_user(follow_question):
                            print("再见！")
                            return
                        new_question = get_user_question_from_input(follow_question)
                        if new_question:
                            current_question = new_question
                            print(f"\n切换到新问题：{current_question}\n")
                            continue
                        else:
                            print("无效追问，继续当前讨论...")
                            continue

                    new_question = get_user_question_from_input(user_input)
                    if new_question:
                        current_question = new_question
                        print(f"\n切换到新问题：{current_question}\n")
                        continue
                    else:
                        print("无效输入，继续当前讨论...")
                        continue

                discussion_context.append(
                    {
                        "question": current_question,
                        "answers": result.get("initial_answers", {}),
                        "advices": result.get("advices", {}),
                    }
                )

                print("\n" + "=" * 50)
                print("当前讨论结果：")
                print(result.get("final_answer", ""))
                print("=" * 50)

                survival_status = result.get("survival_status", "")
                if survival_status:
                    print("\n" + "=" * 50)
                    print("【最终生存状态判断】")
                    print("-" * 50)
                    print("死亡" if survival_status == "死亡" else "存活")
                    print("-" * 50)
                    print("=" * 50)

                followup_options = result.get("followup_options", [])
                followup_map = {str(i + 1): opt for i, opt in enumerate(followup_options)}

                extended_options = None
                if original_choice:
                    extended_options = show_extended_options(original_choice)

                if followup_options:
                    print("\n推荐追问：")
                    for idx, opt in enumerate(followup_options, 1):
                        print(f"  F{idx}. {opt}")

                if extended_options and followup_options:
                    prompt_text = "\n你的选择或问题（输入扩展编号/追问编号F1..，直接输入问题，输入'继续'返回主菜单，或'退出'）："
                elif extended_options:
                    prompt_text = "\n你的选择或问题（输入扩展编号继续深入，直接输入问题，输入'继续'返回主菜单，或'退出'）："
                elif followup_options:
                    prompt_text = "\n你的选择或问题（输入追问编号F1..，直接输入问题，输入'继续'返回主菜单，或'退出'）："
                else:
                    prompt_text = "\n你的选择或问题（直接输入问题继续讨论，输入'继续'返回主菜单，或'退出'）："

                next_input = input(prompt_text).strip()

                if should_exit_by_user(next_input):
                    print("再见！")
                    return

                if next_input.lower() in ["继续", "continue", "c"]:
                    break

                if next_input.lower().startswith("f") and next_input[1:].isdigit():
                    key = next_input[1:]
                    new_question = followup_map.get(key)
                else:
                    new_question = get_user_question_from_input(next_input, extended_options)

                if new_question:
                    current_question = new_question
                    print(f"\n继续讨论：{current_question}\n")
                else:
                    print("无效输入，返回主菜单...")
                    break

            except KeyboardInterrupt:
                print("\n\n程序被中断")
                return
            except Exception as e:
                print(f"\n发生错误：{e}")
                break


if __name__ == "__main__":
    main()

