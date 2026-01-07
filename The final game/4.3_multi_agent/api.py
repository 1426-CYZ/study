import requests

ZHIPU_API_KEY = "22d34b9accc8431c93c9f10afe6a50fb.BZhFFD8JGnkIj2Py"


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
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"API调用失败: {response.status_code}")
