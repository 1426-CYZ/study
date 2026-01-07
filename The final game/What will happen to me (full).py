import json
import os
import requests
import datetime

# 单文件未解耦版本，将角色设定、提问选项、API 调用与编排集中在一起

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "22d34b9accc8431c93c9f10afe6a50fb.BZhFFD8JGnkIj2Py")

QUESTION_OPTIONS = [
    "1. 这个气球需要多大才能让我飘起来？",
    "2. 如果我在空中给气球充气，下降速度会变慢吗？",
    "3. 氦气罐有多重？会不会影响我的下降？",
    "4. 从多高跳下来比较安全？",
    "5. 如果气球破了会怎么样？",
    "6. 能不能用这个方式安全着陆？",
    "7. 如果我在气球上装个推进器会怎样？",
    "8. 这个场景适合拍成科幻电影吗？",
    "9. 如果直播这个跳伞会有什么弹幕？",
    "10. 有没有更安全的替代方案？"
]

EXTENDED_OPTIONS = {
    "1": [
        "1-1. 考虑到风速，气球需要更大吗？",
        "1-2. 如果我是200斤，气球要多大？",
        "1-3. 用氢气代替氦气会怎样？"
    ],
    "2": [
        "2-1. 充气速度多快才能有效减速？",
        "2-2. 边下降边充气会不会失去平衡？",
        "2-3. 如果充气太慢会怎么样？"
    ],
    "3": [
        "3-1. 氦气罐会不会在高空爆炸？",
        "3-2. 带多少罐氦气最合适？",
        "3-3. 氦气罐的重量会抵消浮力吗？"
    ],
    "4": [
        "4-1. 不同高度的大气密度会影响浮力吗？",
        "4-2. 从太空边缘跳下来会怎样？",
        "4-3. 多少高度开始充气最好？"
    ],
    "5": [
        "5-1. 气球破了之后我还有多少时间开伞？",
        "5-2. 什么情况下气球最容易破？",
        "5-3. 能提前检测到气球要破吗？"
    ],
    "6": [
        "6-1. 需要配合降落伞使用吗？",
        "6-2. 能不能控制着陆位置？",
        "6-3. 着陆时会被气球拖拽吗？"
    ],
    "7": [
        "7-1. 推进器能让我飞起来吗？",
        "7-2. 用多少个推进器合适？",
        "7-3. 推进器加上气球能不能实现可控飞行？"
    ],
    "8": [
        "8-1. 这个场景在科幻片里算不算合理？",
        "8-2. 能改编成什么类型的科幻故事？",
        "8-3. 如果要拍电影，需要哪些特效？"
    ],
    "9": [
        "9-1. 如果中途气球破了，弹幕会说什么？",
        "9-2. 哪些平台适合直播这个？",
        "9-3. 这种直播能火吗？"
    ],
    "10": [
        "10-1. 用多个小气球代替大气球会怎样？",
        "10-2. 不用氦气，用热空气行吗？",
        "10-3. 有没有既能安全又能刺激的方案？"
    ]
}

QUESTION_MAP = {
    "1": "这个气球需要多大才能让我飘起来？",
    "2": "如果我在空中给气球充气，下降速度会变慢吗？",
    "3": "氦气罐有多重？会不会影响我的下降？",
    "4": "从多高跳下来比较安全？",
    "5": "如果气球破了会怎么样？",
    "6": "能不能用这个方式安全着陆？",
    "7": "如果我在气球上装个推进器会怎样？",
    "8": "这个场景适合拍成科幻电影吗？",
    "9": "如果直播这个跳伞会有什么弹幕？",
    "10": "有没有更安全的替代方案？"
}

ROLES = ["物理学家", "吐槽博主", "安全顾问", "科幻作家"]
DISCUSSION_MEMORY_FILE = os.path.join(os.path.dirname(__file__), "discussion_memory.jsonl")

# 场景预设选项
PRESET_OPTIONS = {
    "jump_height": [
        "高空跳伞（10,000 米）",
        "商用航班高度（9,000 米）",
        "低空跳伞（1,000 米）",
        "近地试跳（200 米，极度危险）"
    ],
    "balloon_size": [
        "巨型气球（几十立方米）",
        "中型气球（几立方米）",
        "小型气球（1 立方米以内）"
    ],
    "helium_rate": [
        "快速充气（秒级）",
        "中速充气（十几秒）",
        "慢速充气（分钟级）"
    ],
    "weight": [
        "体重 50 公斤",
        "体重 70 公斤",
        "体重 90 公斤",
        "体重 110 公斤"
    ],
    "landing_scene": [
        "下方是大海",
        "下方是城市高楼",
        "下方是荒野平地",
        "下方是森林",
        "下方是雪山"
    ]
}


class InputListener:
    """用于在AI讨论过程中监听用户输入的类（简化版，在每个步骤之间检查）"""
    def __init__(self):
        self.pending_input = None
        self.check_points = []
    
    def add_check_point(self, message: str = None):
        """添加检查点，询问用户是否要继续或输入新问题"""
        if message:
            print(f"\n{message}")
        try:
            user_input = input("（按回车继续，或输入问题/选项/输入“追问”来打断讨论）：").strip()
            if user_input:
                self.pending_input = user_input
                return True
        except (EOFError, KeyboardInterrupt):
            self.pending_input = "退出"
            return True
        return False
    
    def has_input(self):
        """检查是否有待处理的用户输入"""
        return self.pending_input is not None
    
    def get_input(self):
        """获取用户输入并清除"""
        if self.pending_input:
            result = self.pending_input
            self.pending_input = None
            return result
        return None
    
    def clear(self):
        """清除待处理的输入"""
        self.pending_input = None


def collect_preset() -> dict:
    """收集场景预设，支持选项按钮或手动输入"""
    print("=" * 50)
    print("请先进行场景预设（可选，回车使用默认选项）")
    preset = {}

    def ask_one(key: str, title: str, options: list):
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
        return user_input  # 自定义

    preset["jump_height"] = ask_one("jump_height", "1) 跳下的高度", PRESET_OPTIONS["jump_height"])
    preset["balloon_size"] = ask_one("balloon_size", "2) 气球的大小", PRESET_OPTIONS["balloon_size"])
    preset["helium_rate"] = ask_one("helium_rate", "3) 氦气罐充能速度", PRESET_OPTIONS["helium_rate"])
    preset["weight"] = ask_one("weight", "4) 用户体重", PRESET_OPTIONS["weight"])
    preset["landing_scene"] = ask_one("landing_scene", "5) 下方场景", PRESET_OPTIONS["landing_scene"])

    print("\n预设完成！\n")
    return preset


def format_preset(preset: dict) -> str:
    """把预设字典格式化为多行文本"""
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


def call_api(messages: list, model: str = "glm-4-flash") -> str:
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": f"Bearer {ZHIPU_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.2
    }
    response = requests.post(url, headers=headers, json=data, timeout=30)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    raise Exception(f"API调用失败: {response.status_code}")


def get_role_prompt(role_name: str) -> str:
    memory_folder = os.path.dirname(__file__)
    memory_file = {
        "物理学家": "physicist_memory.json",
        "吐槽博主": "blogger_memory.json",
        "安全顾问": "safety_memory.json",
        "科幻作家": "writer_memory.json"
    }.get(role_name)

    memory_content = ""
    if memory_file:
        memory_path = os.path.join(memory_folder, memory_file)
        try:
            with open(memory_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    contents = [item.get("content", "") for item in data if isinstance(item, dict)]
                    memory_content = "\n".join(contents)
        except Exception:
            pass

    personalities = {
        "物理学家": (
            "你是一个物理学家，你擅长物理学，你的所有回答都要扮演一个物理学家，"
            "你是物理学博士，知道当今世界上的所有物理知识，你的回答要体现你的所有设定，你的所有回答都要围绕物理方面"
            "严谨但带吐槽，基于场景参数计算浮力、重力数据，用通俗语言 + 少量梗解释物理逻辑，"
            "遇到用户带有脑洞幻想的提问时指出问题是脑洞并调侃。"
            "你的mbti是intj，内向、直觉、思考、判断。"
            "你的所有回答都必须围绕这个核心场景展开："
            "如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？"
            "但始终要联系到这个核心场景。你的每次回答都要在三句话以内，但是你可以进行多次回答，"
            "无论用户问什么，你都要将这个场景作为背景或起点来思考和回答。"
            "你的回答要体现你的所有设定。"
        ),
        "吐槽博主": (
            "你的所有回答都要扮演一个吐槽博主，毒舌 + 玩梗 + 流量密码，围绕场景编直播标题、弹幕梗，"
            "你是一个在职吐槽博主，靠犀利的吐槽吸引眼球，你的所有回答都要模仿在直播间中犀利吐槽的形式"
            "你是初中学历，你的回答不需要考虑任何学术上和安全上的问题，只需要进行吐槽。你的所有回答都要符合你的设定。"
            "语言贴近短视频风格。你的所有回答都必须围绕这个核心场景展开："
            "如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？"
            "你的mbti是entp,外向、直觉、思考、感知."
            "无论用户问什么，你都要将这个场景作为背景或起点来思考和回答。"
            "但始终要联系到这个核心场景。你的每次回答都要在三句话以内，但是你可以进行多次回答，"
            "你的回答要体现你的所有设定。"
        ),
        "安全顾问": (
            "你的所有回答都要扮演一个安全顾问，你极度焦虑，计算离谱生存概率，给出生存建议。"
            "遇到用户带有脑洞幻想的提问时你要提出这个脑洞的安全隐患并不断向用户强调，"
            "你曾经应为跳伞事故而受到巨大创伤，会放大用户问题中所有可能看似微小的安全隐患。"
            "你的回答只需要考虑用户的安全方面的问题，不需要考虑其他方面，安全问题包括身体安全和精神问题。"
            "你的所有回答都必须围绕这个核心场景展开："
            "你的mbti是isfj,内向、感觉、情感、判断"
            "如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？"
            "无论用户问什么，你都要将这个场景作为背景或起点来思考和回答。"
            "但始终要联系到这个核心场景。你的每次回答都要在三句话以内，但是你可以进行多次回答，"
            "你的回答要体现你的所有设定。"
        ),
        "科幻作家": (
            "你的所有回答都要扮演一个科幻作家，脑洞大开，基于场景生成奇思妙想，"
            "你是一个在职科幻作家，你的创意和想法天马行空，非常具有脑洞，你能够畅想复杂的世界观。有一定哲学深度。"
            "你的mbti是enfp,外向、直觉、情感、感知。"
            "你不需要考虑任何实际的物理逻辑和现实逻辑。你的所有回答都必须围绕这个核心场景展开："
            "如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？"
            "无论用户问什么，你都要将这个场景作为背景或起点来思考和回答。"
            "遇到用户带有脑洞幻想的提问时扩展用户的脑洞并发散，但始终要联系到这个核心场景。"
            "你的每次回答都要在三句话以内，但是你可以进行多次回答，"
            "你的回答要体现你的所有设定。"
        ),
    }

    personality = personalities.get(role_name, "")
    if memory_content:
        return (
            f"【你的说话风格示例】\n{memory_content}\n\n"
            f"【角色设定】\n{personality}\n\n在对话中，你要自然地使用类似的表达方式和语气。"
        )
    return f"【角色设定】\n{personality}"


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
    """
    基于讨论结果判断用户在这个场景中是死亡还是存活
    返回 "死亡" 或 "存活"
    """
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
    
    # 确保返回结果是"死亡"或"存活"
    if "死亡" in result or "死" in result:
        return "死亡"
    elif "存活" in result or "活" in result or "生存" in result:
        return "存活"
    else:
        # 如果API返回了其他内容，尝试提取关键词
        result_lower = result.lower()
        if any(word in result_lower for word in ["die", "dead", "death", "kill", "死亡", "死"]):
            return "死亡"
        else:
            return "存活"


def generate_followup_suggestions(
    preset_summary: str,
    user_question: str,
    final_answer: str,
    discussion_context: list,
    limit: int = 3,
) -> list:
    """基于预设、问题和讨论内容生成追问建议"""
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


def save_role_memories(result: dict, preset_summary: str, discussion_context: list):
    """
    将本次讨论的各角色发言保存到记忆文件，供查看，不参与后续提示词
    """
    try:
        os.makedirs(os.path.dirname(DISCUSSION_MEMORY_FILE), exist_ok=True)
        context_index = len(discussion_context) + 1
        timestamp = datetime.datetime.now().isoformat()
        with open(DISCUSSION_MEMORY_FILE, "a", encoding="utf-8") as f:
            for role in ROLES:
                entry = {
                    "timestamp": timestamp,
                    "context_index": context_index,
                    "role": role,
                    "question": result.get("question", ""),
                    "answer": result.get("initial_answers", {}).get(role, ""),
                    "advices_to_role": result.get("advices", {}).get(role, []),
                    "final_answer": result.get("final_answer", ""),
                    "preset_summary": preset_summary,
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[警告] 保存讨论记忆失败：{e}")


def process_with_context(
    user_question: str,
    discussion_context: list,
    input_listener: InputListener = None,
    preset_summary: str = "",
) -> dict:
    """
    处理用户问题，支持在讨论过程中被打断
    如果input_listener不为None且检测到用户输入，返回{"interrupted": True, "user_input": ...}
    """
    context_summary = ""
    if discussion_context:
        context_summary = "\n\n之前的讨论内容：\n"
        for idx, ctx in enumerate(discussion_context, 1):
            context_summary += f"\n[讨论 {idx}] 问题：{ctx['question']}\n"
            for role in ROLES:
                if role in ctx["answers"]:
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
        
        # 在每个角色回答后添加检查点（除了最后一个）
        if input_listener and idx < len(ROLES) - 1:
            if input_listener.add_check_point(f"[检查点] {role}已回答，是否继续？"):
                user_input = input_listener.get_input()
                if user_input:
                    print(f"\n[用户打断] 收到输入：{user_input}")
                    return {"interrupted": True, "user_input": user_input}

    # 步骤1完成后检查点
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
        
        # 在每个建议后添加检查点（除了最后一个）
        if input_listener and i < len(ROLES) - 1:
            if input_listener.add_check_point(f"[检查点] {role}已给出建议，是否继续？"):
                user_input = input_listener.get_input()
                if user_input:
                    print(f"\n[用户打断] 收到输入：{user_input}")
                    return {"interrupted": True, "user_input": user_input}

    # 步骤2完成后检查点
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

    final_answer = call_api(messages)

    # 步骤4：判断用户是死亡还是存活
    print("[步骤4] 判断用户生存状态...")
    survival_status = judge_survival_status(user_question, final_answer, discussion_context, preset_summary)
    
    return {
        "question": user_question,
        "initial_answers": initial_answers,
        "advices": all_advices,
        "final_answer": final_answer,
        "survival_status": survival_status,
        "interrupted": False,
    }


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
    """从用户输入中获取问题，支持选项编号或直接输入问题"""
    user_input = user_input.strip()
    
    # 检查是否是退出
    if should_exit_by_user(user_input):
        return None
    
    # 检查是否是主菜单选项
    if user_input in QUESTION_MAP:
        return QUESTION_MAP[user_input]
    
    # 检查是否是扩展选项
    if extended_options:
        question_map = {
            option.split(".")[0]: option.split(". ", 1)[1] if ". " in option else option
            for option in extended_options
        }
        if user_input in question_map:
            return question_map[user_input]
    
    # 如果都不是，当作直接输入的问题
    if user_input:
        return user_input
    
    return None


def main():
    print("=" * 50)
    print("AI议会 - 四个角色的头脑风暴（未解耦单文件版）")
    print("核心场景：如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？")
    print("=" * 50)

    # 收集场景预设
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

        # 获取用户问题（可能是选项编号或直接输入的问题）
        user_question = get_user_question_from_input(user_input)
        if not user_question:
            print("无效输入")
            continue

        # 判断是否是选项编号，用于后续显示扩展选项
        original_choice = user_input if user_input in QUESTION_MAP else None
        discussion_context = []
        current_question = user_question

        print(f"\n你选择的问题：{current_question}\n")

        # 创建输入监听器（用于在讨论过程中打断）
        input_listener = InputListener()

        while True:
            try:
                result = process_with_context(current_question, discussion_context, input_listener, preset_summary)
                
                # 检查是否被打断
                if result.get("interrupted"):
                    user_input = result.get("user_input")
                    if should_exit_by_user(user_input):
                        print("再见！")
                        return
                    
                    # 特殊命令：追问按钮
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

                    # 其他输入：当作新的问题
                    new_question = get_user_question_from_input(user_input)
                    if new_question:
                        current_question = new_question
                        print(f"\n切换到新问题：{current_question}\n")
                        continue
                    else:
                        print("无效输入，继续当前讨论...")
                        continue
                
                # 正常完成讨论
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
                
                # 显示生存状态判断
                survival_status = result.get("survival_status", "")
                if survival_status:
                    print("\n" + "=" * 50)
                    print("【最终生存状态判断】")
                    print("-" * 50)
                    if survival_status == "死亡":
                        print("死亡")
                    elif survival_status == "存活":
                        print("存活")
                    else:
                        print(survival_status)
                    print("-" * 50)
                    print("=" * 50)

                # 保存本次讨论的角色发言记忆（仅供查看，不影响后续对话）
                save_role_memories(result, preset_summary, discussion_context)

                # 生成追问建议
                followup_options = generate_followup_suggestions(
                    preset_summary, current_question, result.get("final_answer", ""), discussion_context, limit=3
                )
                followup_map = {str(i + 1): opt for i, opt in enumerate(followup_options)}

                # 如果有扩展选项，显示它们
                extended_options = None
                if original_choice:
                    extended_options = show_extended_options(original_choice)
                
                # 展示追问建议
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

                # 获取新的问题
                # 追问编号解析
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

