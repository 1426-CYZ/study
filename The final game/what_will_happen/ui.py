from .config import QUESTION_OPTIONS, EXTENDED_OPTIONS, QUESTION_MAP
from .logic import should_exit_by_user


def show_options():
    print("\n请选择一个问题（输入数字 1-10，直接输入问题，或输入'退出'结束）：")
    for option in QUESTION_OPTIONS:
        print(f"  {option}")
    print("  或者直接输入你的问题")


def show_extended_options(original_choice: str) -> list:
    options = EXTENDED_OPTIONS.get(original_choice, [])
    if not options:
        return None

    print("\n" + "=" * 50)
    print("你想继续深入了解哪个方面？")
    print("（输入选项编号继续深入讨论，直接输入问题，输入'继续'返回主菜单，或'退出'结束）")
    for option in options:
        print(f"  {option}")
    print("  或者直接输入你的问题")
    return options


def get_user_question_from_input(user_input: str, extended_options: list = None) -> str:
    user_input = user_input.strip()
    if should_exit_by_user(user_input):
        return None

    if user_input in QUESTION_MAP:
        return QUESTION_MAP[user_input]

    if extended_options:
        question_map = {
            option.split(".")[0]: option.split(". ", 1)[1] if ". " in option else option
            for option in extended_options
        }
        if user_input in question_map:
            return question_map[user_input]

    if user_input:
        return user_input
    return None

