
import { GoogleGenAI, Type } from "@google/genai";
import { PresetData, Role } from "../types";

// Always use const ai = new GoogleGenAI({apiKey: process.env.API_KEY});.
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

export async function getRoleResponse(
  role: Role, 
  question: string, 
  preset: PresetData,
  history: string = ""
): Promise<string> {
  // Use gemini-3-flash-preview for general text tasks.
  const model = "gemini-3-flash-preview";
  const prompt = `
    你现在扮演：${role.title} (${role.name})。
    设定：${role.personality}
    核心背景：如果我背着几罐氦气和一个巨大的未充气的气球从飞机上跳下来会怎么样？
    当前场景参数：高度-${preset.jumpHeight}, 气球-${preset.balloonSize}, 充气速度-${preset.heliumRate}, 体重-${preset.weight}, 着陆点-${preset.landingScene}。
    
    用户的问题是：${question}
    ${history ? `之前的讨论背景：${history}` : ""}
    
    请以此角色身份回答。注意：
    1. 必须符合人设。
    2. 每次发言必须在3句话以内。
    3. 风格要有趣、鲜明。
    
    直接给出回答内容，不要包含角色名字或其他无关信息。
  `;

  try {
    // Correct usage of generateContent for simple text generation.
    const response = await ai.models.generateContent({
      model,
      contents: prompt,
      config: { temperature: 0.8 }
    });
    // response.text is a property, not a method.
    return response.text || "……（陷入沉思）";
  } catch (error) {
    console.error("API Error:", error);
    return "信号不好，我刚才没听清。";
  }
}

export async function getSurvivalSummary(
  question: string,
  discussion: string,
  preset: PresetData
): Promise<{ summary: string; status: '生存' | '死亡' }> {
  const model = "gemini-3-flash-preview";
  const prompt = `
    根据以下场景和讨论内容，做一个最终总结，并判断用户的生存状态。
    场景：跳伞氦气球实验。参数：${JSON.stringify(preset)}
    问题：${question}
    讨论记录：${discussion}
    
    输出要求：
    1. 总结讨论核心要点。
    2. 给出最终判定：存活或死亡。
    
    请按JSON格式返回：
    {
      "summary": "一段话总结结论",
      "status": "存活" 或 "死亡"
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model,
      contents: prompt,
      config: { 
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            summary: { type: Type.STRING, description: "A summary of the discussion conclusions." },
            status: { type: Type.STRING, description: "Final survival status, either '存活' or '死亡'." }
          },
          required: ["summary", "status"],
          propertyOrdering: ["summary", "status"],
        }
      }
    });
    // Ensure the response is trimmed before parsing. response.text is a property.
    const result = JSON.parse(response.text?.trim() || "{}");
    return {
      summary: result.summary || "讨论结束了，结果扑朔迷离。",
      status: result.status === '死亡' ? '死亡' : '生存'
    };
  } catch (error) {
    console.error("Summary API Error:", error);
    return { summary: "系统过载，无法得出定论。", status: '生存' };
  }
}

export async function generateFollowupOptions(
  question: string,
  discussion: string
): Promise<string[]> {
  const model = "gemini-3-flash-preview";
  const prompt = `
    基于当前关于“跳伞氦气球”的讨论：
    原问题：${question}
    内容：${discussion}
    
    请生成3个简短有趣的追问建议，每个不超过15个字。
    以数组格式返回JSON。
  `;

  try {
    const response = await ai.models.generateContent({
      model,
      contents: prompt,
      config: { 
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.ARRAY,
          items: { type: Type.STRING }
        }
      }
    });
    // response.text is a property.
    return JSON.parse(response.text?.trim() || "[]");
  } catch (error) {
    console.error("Followup API Error:", error);
    return ["如果氦气漏了呢？", "能用来载货吗？", "有没有更刺激的方案？"];
  }
}
