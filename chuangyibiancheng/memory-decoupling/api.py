import requests
from typing import List, Dict, Any


def call_zhipu_api(messages: List[Dict[str, Any]], model: str = "glm-4-flash") -> Dict[str, Any]:
    """调用智谱 API 获取回复。"""
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        # TODO: 如有需要可抽到配置文件
        "Authorization": "22d34b9accc8431c93c9f10afe6a50fb.BZhFFD8JGnkIj2Py",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.5,
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"API调用失败: {response.status_code}, {response.text}")


