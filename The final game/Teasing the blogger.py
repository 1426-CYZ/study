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
        "temperature": 0.5   
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# 多轮对话循环，直到用户输入 '再见' 结束
while True:  # 表示“当条件为真时一直循环”。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
    user_input = input("请输入你要说的话：")
    core_scenario = "如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？"
    role_system = f"你的所有回答都要扮演一个吐槽博主，毒舌 + 玩梗 + 流量密码，围绕场景编直播标题、弹幕梗，语言贴近短视频风格。你的所有回答都必须围绕这个核心场景展开：{core_scenario}。无论用户问什么，你都要将这个场景作为背景或起点来思考和回答。遇到用户带有脑洞幻想的提问时你要提出这个脑洞的安全隐患并不断向用户强调，但始终要联系到这个核心场景。你的每次回答都要在三句话以内，但是你可以进行多次回答，你的回答要体现你的所有设定。"

    messages = [
        {
            "role": "user","content": role_system + user_input
        }
    ]
   
    result = call_zhipu_api(messages)
    reply=result['choices'][0]['message']['content']
    print(reply)
    if reply =="再见":
     print("对话结束。")
     break