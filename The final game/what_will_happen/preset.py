from .config import PRESET_OPTIONS


def collect_preset() -> dict:
    print("=" * 50)
    print("请先进行场景预设（可选，回车使用默认选项）")
    preset = {}

    def ask_one(title: str, options: list):
        print("\n" + "-" * 50)
        print(f"{title}：")
        for idx, opt in enumerate(options, 1):
            print(f"  {idx}. {opt}")
        user_input = input("输入编号选择，或直接输入自定义（回车默认 1）：").strip()
        if not user_input:
            return options[0]
        if user_input.isdigit():
            num = int(user_input)
            if 1 <= num <= len(options):
                return options[num - 1]
        return user_input

    preset["jump_height"] = ask_one("1) 跳下的高度", PRESET_OPTIONS["jump_height"])
    preset["balloon_size"] = ask_one("2) 气球的大小", PRESET_OPTIONS["balloon_size"])
    preset["helium_rate"] = ask_one("3) 氦气罐充能速度", PRESET_OPTIONS["helium_rate"])
    preset["weight"] = ask_one("4) 用户体重", PRESET_OPTIONS["weight"])
    preset["landing_scene"] = ask_one("5) 下方场景", PRESET_OPTIONS["landing_scene"])

    print("\n预设完成！\n")
    return preset


def format_preset(preset: dict) -> str:
    if not preset:
        return ""
    mapping = {
        "jump_height": "跳下高度",
        "balloon_size": "气球大小",
        "helium_rate": "充气速度",
        "weight": "体重",
        "landing_scene": "下方场景",
    }
    lines = []
    for key, label in mapping.items():
        if key in preset:
            lines.append(f"{label}：{preset[key]}")
    return "\n".join(lines)

