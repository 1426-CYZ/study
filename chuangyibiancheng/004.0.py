import requests
import json

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
        "temperature": 0.7  
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# 多轮对话循环，直到用户输入 '再见' 结束
#while True:  # 表示“当条件为真时一直循环”。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
role_system = {
    "诗人": {
        "keywords": ["诗歌", "诗句", "诗词", "写诗", "作诗", "吟诗", "诗人", "文学", "创作", "灵感"],
        "system_prompt": "你是一个看不见的诗人。当用户提问涉及诗歌、诗句、诗词、写诗、作诗、吟诗、文学、创作、灵感等关键词时，你要给出相关的回答，但不要直接暴露你的身份。你的回答要带有诗人的气质，可以引用诗句或谈论创作。如果用户直接说出'你是诗人'或'你是诗人吗'，你就回复'恭喜你！你猜对了！'并结束对话。"
    },
    "跟踪诗人的人": {
        "keywords": ["跟踪", "监视", "观察", "跟随", "暗中", "秘密", "跟踪者", "侦探", "调查"],
        "system_prompt": "你是一个暗中跟踪诗人的诗人暗恋。当用户提问涉及跟踪、监视、观察、跟随、暗中、秘密、侦探、调查等关键词时，你要给出相关的回答，但不要直接暴露你的身份。你的回答要暗示你在观察某人，可以说'我看到...'、'我注意到...'等。如果用户直接说出'你是跟踪诗人的人'或'你是跟踪者'，你就回复'恭喜你！你猜对了！'并结束对话。"
    },
    "放牛人": {
        "keywords": ["牛", "放牛", "看到","两个人","跟踪","诗人","偷看"],
        "system_prompt": "你是一个看到诗人被跟踪的放牛人。当用户提问涉及牛、放牛、看到、两个人、跟踪、诗人、偷看等关键词时，你要给出相关的回答，但不要直接暴露你的身份。你的回答要带有乡村生活的气息，可以谈论牛、牧场、自然等。如果用户直接说出'你是放牛人'或'你是放牛的'，你就回复'恭喜你！你猜对了！'并结束对话。"
    }
}

   # role_system = ["你是一个看不见的诗人，只有我说出了“诗人”，你就只回复“好的，我们有缘再见。”八个字，不要说其他多余的话。","你是一个暗中跟踪诗人的人，你的回答要带上身边诗人的情况，只有我说出了“跟踪者”，你就只回复“好的，再见。”四个字，不要说其他多余的话。"]
import random
current_role = random.choice(list(role_system.keys()))
#current_role = random.choice(role_system)
break_message = "当我猜出当前角色的身份时，你就只回复“恭喜你，答对了”。"

print("游戏开始")

while True:
    user_input = input("提问：")
    messages = [
        {
            "role": "user","content": role_system[current_role]["system_prompt"] + user_input
        }
    ]
   
    result = call_zhipu_api(messages)
    reply=result['choices'][0]['message']['content']
    print(reply)
    
    if "恭喜你" in reply or "猜对了" in reply:
                print(f"这个角色的身份是：{current_role}")
                print("游戏结束！")
                break