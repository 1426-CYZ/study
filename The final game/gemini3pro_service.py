import os
import json
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    raise RuntimeError("请先在环境变量中设置 GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

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

class ChatRequest(BaseModel):
    question: str
    preset: Optional[Dict[str, str]] = None
    history: Optional[List[Dict[str, Any]]] = None
    model: str = "gemini-1.5-pro"

app = FastAPI()

def build_prompt(req: ChatRequest) -> str:
    preset_summary = ""
    if req.preset:
        preset_summary = "\n".join([f"{k}：{v}" for k, v in req.preset.items()])
    history_text = ""
    if req.history:
        parts = []
        for h in req.history:
            role = h.get("role", "user")
            content = h.get("content", "")
            parts.append(f"{role}: {content}")
        history_text = "\n".join(parts)
    prompt_parts = [
        "核心场景：如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？",
        f"【场景预设】\n{preset_summary}" if preset_summary else "",
        f"【历史对话】\n{history_text}" if history_text else "",
        f"用户问题：{req.question}",
        "请基于场景预设给出回答，要求简洁、具体。"
    ]
    return "\n\n".join([p for p in prompt_parts if p.strip()])

def call_gemini(prompt: str, model: str) -> str:
    gemini_model = genai.GenerativeModel(model)
    response = gemini_model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0.2))
    if hasattr(response, "text"):
        return response.text
    try:
        return "".join(part.text for part in response.candidates[0].content.parts)
    except Exception as e:
        raise RuntimeError(f"Gemini 调用失败: {e}")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/options")
def options():
    return {"questions": QUESTION_OPTIONS, "extended": EXTENDED_OPTIONS, "presets": PRESET_OPTIONS}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        prompt = build_prompt(req)
        answer = call_gemini(prompt, req.model)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("gemini3pro_service:app", host="0.0.0.0", port=8000, reload=False)

