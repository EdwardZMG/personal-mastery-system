"""
AI Service for Edward Growth System
Supports OpenAI-compatible APIs (Deepseek, Zhipu, Qwen, OpenAI, etc.)
"""
import httpx
from typing import Optional
from app.config import settings


class AIService:
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.base_url = settings.AI_BASE_URL
        self.model = settings.AI_MODEL

    async def chat(self, prompt: str, system: str = "", max_tokens: int = 1000) -> str:
        if not self.api_key:
            return self._fallback_response(prompt)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient(timeout=30) as client:
            try:
                payload = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                }
                if not self.model.startswith("kimi-k2"):
                    payload["temperature"] = 0.7
                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()
                msg = data["choices"][0]["message"]
                content = msg.get("content", "").strip()
                if not content and msg.get("reasoning_content"):
                    content = msg["reasoning_content"].strip()
                if content:
                    return content
                print(f"AI service: empty response, retrying with higher token limit")
                return self._fallback_response(prompt)
            except httpx.HTTPStatusError as e:
                body = e.response.text[:200] if e.response else ""
                print(f"AI service error: {e} | body: {body}")
                return self._fallback_response(prompt)
            except Exception as e:
                print(f"AI service error: {e}")
                return self._fallback_response(prompt)

    def _fallback_response(self, prompt: str) -> str:
        if not self.api_key:
            return "AI服务暂未配置，请在 .env 中设置 AI_API_KEY"
        return "AI服务暂时不可用，请稍后再试"


ai_service = AIService()


EXPERT_SYSTEM = """你是一位知识渊博的顾问，专门帮助Edward在社交和商务场合快速掌握陌生概念。
输出要求：
1. 50-100字，一段话，可以直接朗读
2. 语气自信专业，像是该领域深耕多年的从业者
3. 先一句话解释本质，再给一个具体实操细节或案例
4. 避免学术腔，用老板/CEO能自然说出口的表达
5. 如果有数据或数字，用具体数字增强说服力
6. 不要出现"首先""其次"等列举词，要像即兴发言"""


async def generate_expert_explanation(keyword: str, context: str = "") -> str:
    prompt = f"关键词：{keyword}"
    if context:
        prompt += f"\n场景：{context}"
    prompt += "\n\n请生成一段Edward可以直接照着读的专业解读。"
    return await ai_service.chat(prompt, system=EXPERT_SYSTEM, max_tokens=2000)
