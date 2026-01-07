from orchestrator import process_with_context
from logic import should_exit_by_user
from config import QUESTION_OPTIONS, EXTENDED_OPTIONS, QUESTION_MAP


def show_options():
    print("\n请选择一个问题（输入数字 1-10，或输入'退出'结束）：")
    for option in QUESTION_OPTIONS:
        print(f"  {option}")


def get_question_by_choice(choice: str) -> str:
    return QUESTION_MAP.get(choice.strip())


def show_extended_options(original_choice: str) -> list:
    options = EXTENDED_OPTIONS.get(original_choice, [])
    if not options:
        return None

    print("\n" + "=" * 50)
    print("你想继续深入了解哪个方面？")
    print("（输入选项编号继续深入讨论，输入'继续'返回主菜单，或'退出'结束）")
    for option in options:
        print(f"  {option}")
    return options


def get_extended_question(choice: str, extended_options: list) -> str:
    if not extended_options:
        return None

    question_map = {
        option.split('.')[0]: option.split('. ', 1)[1] if '. ' in option else option
        for option in extended_options
    }
    return question_map.get(choice.strip())


def main():
    print("=" * 50)
    print("AI议会 - 四个角色的头脑风暴")
    print("核心场景：如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？")
    print("=" * 50)

    while True:
        show_options()
        user_input = input("\n你的选择：").strip()

        if should_exit_by_user(user_input):
            print("再见！")
            break

        if not user_input:
            continue

        user_question = get_question_by_choice(user_input)
        if not user_question:
            print("无效选择，请输入 1-10 的数字")
            continue

        original_choice = user_input
        discussion_context = []
        current_question = user_question

        print(f"\n你选择的问题：{current_question}\n")

        while True:
            result = process_with_context(current_question, discussion_context)
            discussion_context.append({
                "question": current_question,
                "answers": result['initial_answers'],
                "advices": result['advices']
            })

            print("\n" + "=" * 50)
            print("当前讨论结果：")
            print(result['final_answer'])
            print("=" * 50)

            extended_options = show_extended_options(original_choice)

            if not extended_options:
                break

            next_input = input("\n你的选择（输入选项编号继续深入，或'继续'返回主菜单，或'退出'）：").strip()

            if should_exit_by_user(next_input):
                print("再见！")
                return

            if next_input.lower() in ['继续', 'continue', 'c']:
                break

            extended_question = get_extended_question(next_input, extended_options)
            if extended_question:
                current_question = extended_question
                print(f"\n继续深入讨论：{current_question}\n")
            else:
                print("无效选择，返回主菜单...")
                break


if __name__ == "__main__":
    main()
