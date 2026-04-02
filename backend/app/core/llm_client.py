"""
MiniMax LLM 客户端
文档: https://platform.minimax.io/document
"""

import os
import json
import requests
from typing import Optional, Dict, Any, List


class MiniMaxClient:
    """MiniMax API 客户端"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        if not self.api_key:
            raise ValueError("MINIMAX_API_KEY is required")
        self.base_url = "https://api.minimax.chat/v1"
        self.model = "abab6.5s-chat"

    def chat(
        self,
        prompt: str,
        system_prompt: str = "你是一个专业的室内装修顾问，请根据知识库内容回答用户问题。",
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """调用对话接口"""
        url = f"{self.base_url}/text/chatcompletion_v2"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "")

    def chat_with_context(
        self,
        user_input: str,
        context: List[Dict[str, Any]],
        system_prompt: str = None
    ) -> str:
        """基于知识库上下文对话"""
        if system_prompt is None:
            system_prompt = """你是一个专业的室内装修顾问。
根据下面提供的知识库内容回答用户问题。
如果知识库中没有相关信息，请基于你的专业知识回答，但要说明这是通用建议。"""

        # 构建上下文
        context_text = "\n\n".join([
            f"【{item.get('source', '未知来源')}】{item.get('content', '')}"
            for item in context
        ])

        full_prompt = f"""参考知识库内容：
{context_text}

用户问题：{user_input}

请根据以上知识库内容回答用户问题。"""

        return self.chat(full_prompt, system_prompt)

    def generate_image_prompt(
        self,
        style: str,
        room_type: str,
        requirements: str = ""
    ) -> str:
        """生成 AI 绘画提示词"""
        system_prompt = """你是一个专业的室内设计提示词工程师。
根据用户需求生成详细、准确的 AI 绘画提示词。
输出格式要求：中英文混合，描述详细，包含风格、材质、色彩、光线等要素。"""

        prompt = f"""请为以下装修需求生成 AI 绘画提示词：

- 装修风格：{style}
- 房间类型：{room_type}
- 特殊需求：{requirements if requirements else '无'}

请生成详细的中文提示词，包含：
1. 整体氛围描述
2. 色彩搭配
3. 主要家具
4. 材质质感
5. 光线效果
6. 细节装饰

直接输出提示词，不要其他说明。"""

        return self.chat(prompt, system_prompt)

    def analyze_image(
        self,
        image_url: str = None,
        image_base64: str = None,
        prompt: str = None
    ) -> str:
        """图像理解（需要支持 vision 的模型）"""
        # MiniMax 当前版本可能不支持 vision，暂时返回占位
        # 后续可接入其他支持 vision 的 API
        if prompt is None:
            prompt = "请详细描述这张图片中的房间布局、装修风格、家具摆放等信息。"

        # TODO: 实现 vision 支持
        return "图像理解功能需要支持 vision 的 API，请先配置支持 vision 的模型。"


# 全局实例
_llm_client = None


def get_llm_client() -> MiniMaxClient:
    """获取 LLM 客户端单例"""
    global _llm_client
    if _llm_client is None:
        _llm_client = MiniMaxClient()
    return _llm_client