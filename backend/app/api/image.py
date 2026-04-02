"""
图像理解 API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.core.llm_client import get_llm_client

router = APIRouter(prefix="/image", tags=["image"])


class ImageAnalyzeRequest(BaseModel):
    """图像理解请求"""
    image_base64: Optional[str] = None
    image_url: Optional[str] = None
    analyze_type: str = "layout"


class ImageAnalyzeResponse(BaseModel):
    """图像理解响应"""
    description: str
    layout: dict
    suggestions: list


@router.post("/analyze")
async def analyze_image(request: ImageAnalyzeRequest):
    """分析户型图或房间照片"""
    try:
        llm = get_llm_client()

        # MiniMax 当前版本可能不支持 vision
        # 暂时返回提示信息
        return ImageAnalyzeResponse(
            description="图像理解功能需要支持 vision 的 API。当前 MiniMax 模型暂不支持图像理解，请使用支持 vision 的 API（如 GPT-4V、Claude Vision）。",
            layout={},
            suggestions=[]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vision-status")
async def vision_status():
    """检查视觉理解能力状态"""
    return {
        "vision_enabled": False,
        "reason": "MiniMax 当前模型暂不支持 vision",
        "alternatives": [
            "OpenAI GPT-4 Vision",
            "Claude Vision",
            "Google Gemini Vision"
        ]
    }