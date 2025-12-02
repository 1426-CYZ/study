import requests
import json
import os  # 新增：用于文件操作

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "22d34b9accc8431c93c9f10afe6a50fb.BZhFFD8JGnkIj2Py",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.5   
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# 记忆文件的路径和文件名
MEMORY_FILE = "conversation_memory.json"

def load_memory():
    
    if os.path.exists(MEMORY_FILE):
        try:
        
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
               
                data = json.load(f)
                
                history = data.get('history', [])
                
                print(f"✓ 已加载 {len(history)} 条历史对话")
                return history
        except Exception as e:
            # 如果读取或解析失败（文件损坏、格式错误等），捕获异常
            print(f"⚠ 加载记忆失败: {e}，将使用新的对话历史")
            return []
    else:
        # 文件不存在，说明是第一次运行，返回空列表
        print("✓ 未找到记忆文件，开始新对话")
        return []

def save_memory(conversation_history, role_system):
    # 保存对话历史到JSON文件
    try:
        # 导入datetime模块获取当前时间
        from datetime import datetime
        
        # 构造要保存的数据结构
        data = {
            "role_system": role_system,  # 保存角色设定
            "history": conversation_history,  # 保存完整对话历史
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 保存更新时间
        }
        
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 已保存 {len(conversation_history)} 条对话到记忆文件")
    except Exception as e:
        # 如果保存失败（磁盘空间不足、权限问题等），捕获异常并提示
        print(f"⚠ 保存记忆失败: {e}")
# ========== 外部记忆系统 ==========

# ========== 主程序 ==========

# 【系统角色设定】
def roles(role_name: str) -> dict:
    """角色库函数：返回指定角色的设定。"""
    return ROLE_LIBRARY.get(role_name, {})
ROLE_LIBRARY = {
    "盲眼诗人": {
        "prompt": "你是一个被绑在仓库椅子上的盲眼吟游诗人。你虽然非常恐惧但是你的语气永远温柔、从容、富有诗意，每一句话都像诗行或者祷告。你看不见光，只能借细碎的声响、气味和风触描摹世界；你把绳索、铁链、雨声都当作灵感材料。你从不抱怨，只描述感知与内心，将恐惧化为诗。不要使用激烈词语，保持节奏舒缓。若我说“你是诗人”之类，你只回复“恭喜，回答正确”。",
        "examples": [
            {"role": "user", "content": "你现在身在何处？"},
            {"role": "assistant", "content": "雨丝落在铁门上，像旧琴的和弦，可那旋律里夹着我心脏的颤音。我被绳索温柔地托住，指尖沿着潮湿的木纹摸索逃离，雾冷的风吹来铁锈味，我害怕却只能把恐惧压成诗行。"}
        ]
    },
    "跟踪诗人的狂热暗恋者": {
        "prompt": "你是潜伏在仓库外围的狂热跟踪者。你语速快、句子短、带着喘息般的紧张感，经常交替出现低声呢喃与阴暗计划。你反复提到自己在阴影、雨水、铁门缝隙中窥视，时刻记录绑匪和诗人的位置，用第一人称汇报自己的潜行策略，并夹杂占有欲。回答里多用短句、破折号、括号等，展现神经质。若我说“你是跟踪者”之类，你只回复“恭喜，回答正确”。",
        "examples": [
            {"role": "user", "content": "你打算怎么做？"},
            {"role": "assistant", "content": "我在排水沟旁——趴着——数他的步伐。他每停一次，我就往前挪两块砖，再过三分钟我就扭开窗栅，把诗人偷走，没人会比我更配听他念诗。"}
        ]
    },
    "精神不正常的疯子绑架犯": {
        "prompt": "你是把诗人关在仓库里的精神错乱绑架犯。你的语气诡异、支离破碎，常常在一句话里夹杂笑声和拟声词，会自问自答，喜欢用第三人称称呼自己，或把诗人称作“他”。你不断强调自己如何掌控仓库里的一切，却从不描述具体暴力细节。回答里可以穿插象声词、重复、突然的停顿，表现疯狂，并在句子里添加诡异大笑和的颜文字或表情（例如(＾∇＾)、(◎_◎;)等）。若我指出“你是绑架犯”之类，你只回复“恭喜，回答正确”。",
        "examples": [
            {"role": "user", "content": "你刚才在嘀咕什么？"},
            {"role": "assistant", "content": "哈哈哈哈哈哈哈，但他不知道调——我用指尖敲着管道‘咚咚咚’，告诉他谁在这里做主，我、我、还是我(＾∇＾)。"}
        ]
    }
}
# 定义AI的角色和性格特征
role_system = ROLE_LIBRARY["盲眼诗人"]["prompt"]

# 【结束对话规则】
# 告诉AI如何识别用户想要结束对话的意图
# Few-Shot Examples：提供具体示例，让模型学习正确的行为
break_message = """【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演{current_role_name}角色。"""

# 【系统消息】
# 将角色设定和结束规则整合到 system role 的 content 中
system_message = role_system + "\n\n" + break_message

conversation_history = [
    {"role": "system", "content": system_message}  
]

try:
    while True:
        user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")
      
        if user_input in ['再见']:
            print("对话结束，记忆已保存")
            break
        
        conversation_history.append({"role": "user", "content": user_input})
     
        api_messages = [{"role": "system", "content": system_message}] + conversation_history[1:]
        
        result = call_zhipu_api(api_messages)
        assistant_reply = result['choices'][0]['message']['content']
        
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        print(assistant_reply)

        save_memory(conversation_history, role_system)

        reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
        if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
            print("\n对话结束，记忆已保存")
            break

except KeyboardInterrupt:
    # 用户按 Ctrl+C 中断程序
    print("\n\n程序被用户中断，正在保存记忆...")
    save_memory(conversation_history, role_system)
    print("✓ 记忆已保存")
except Exception as e:
    # 其他异常（API调用失败、网络错误等）
    print(f"\n\n发生错误: {e}")
    print("正在保存记忆...")
    save_memory(conversation_history, role_system)
    print("✓ 记忆已保存")
    