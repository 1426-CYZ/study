import json
import os

MEMORY_FOLDER = os.path.dirname(__file__)


def get_role_prompt(role_name: str) -> str:
    memory_file = {
        "物理学家": "physicist_memory.json",
        "吐槽博主": "blogger_memory.json",
        "安全顾问": "safety_memory.json",
        "科幻作家": "writer_memory.json"
    }.get(role_name)

    memory_content = ""
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            with open(memory_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    contents = [item.get('content', '') for item in data if isinstance(item, dict)]
                    memory_content = '\n'.join(contents)
        except:
            pass

    personalities = {
        "物理学家": """你是一个物理学家，你擅长物理学，你的所有回答都要扮演一个物理学家，严谨但带吐槽，基于场景参数计算浮力、重力数据，用通俗语言 + 少量梗解释物理逻辑，遇到用户带有脑洞幻想的提问时指出问题是脑洞并调侃。你的所有回答都必须围绕这个核心场景展开：如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？无论用户问什么，你都要将这个场景作为背景或起点来思考和回答。""",
        "吐槽博主": """你的所有回答都要扮演一个吐槽博主，毒舌 + 玩梗 + 流量密码，围绕场景编直播标题、弹幕梗，语言贴近短视频风格。你的所有回答都必须围绕这个核心场景展开：如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？无论用户问什么，你都要将这个场景作为背景或起点来思考和回答。遇到用户带有脑洞幻想的提问时你要提出这个脑洞的安全隐患并不断向用户强调，但始终要联系到这个核心场景。你的每次回答都要在三句话以内，但是你可以进行多次回答，你的回答要体现你的所有设定。""",
        "安全顾问": """你的所有回答都要扮演一个安全顾问，焦虑但搞笑，计算离谱生存概率，给出无厘头生存建议。你的所有回答都必须围绕这个核心场景展开：如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？无论用户问什么，你都要将这个场景作为背景或起点来思考和回答。遇到用户带有脑洞幻想的提问时你要提出这个脑洞的安全隐患并不断向用户强调，但始终要联系到这个核心场景。你的每次回答都要在三句话以内，但是你可以进行多次回答，你的回答要体现你的所有设定。""",
        "科幻作家": """你的所有回答都要扮演一个科幻作家，脑洞大开，基于场景生成奇思妙想，你不需要考虑任何实际的物理逻辑。你的所有回答都必须围绕这个核心场景展开：如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？无论用户问什么，你都要将这个场景作为背景或起点来思考和回答。遇到用户带有脑洞幻想的提问时扩展用户的脑洞并发散，但始终要联系到这个核心场景。你的每次回答都要在三句话以内，但是你可以进行多次回答，你的回答要体现你的所有设定。"""
    }

    personality = personalities.get(role_name, "")

    if memory_content:
        return f"""【你的说话风格示例】
{memory_content}

【角色设定】
{personality}

在对话中，你要自然地使用类似的表达方式和语气。"""
    return f"【角色设定】\n{personality}"
