"""
提示词生成 API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.core.knowledge_base import get_knowledge_base

router = APIRouter(prefix="/prompt", tags=["prompt"])


class PromptGenerateRequest(BaseModel):
    """提示词生成请求"""
    style: str
    room_type: str
    requirements: Optional[str] = ""
    mood: Optional[str] = ""
    color_preference: Optional[str] = ""


class PromptGenerateResponse(BaseModel):
    """提示词生成响应"""
    prompt_zh: str
    prompt_en: str
    style_info: Dict[str, Any]
    recommended_items: List[str]


# 预置提示词模板
PROMPT_TEMPLATES = {
    "奶油风": {
        "zh": "奶油色客厅，现代简约风格，浅米色布艺沙发，原木色茶几，柔和灯光，大白墙，温馨舒适氛围，居家生活场景",
        "en": "cream colored living room, modern minimalist style, beige fabric sofa, natural wood coffee table, soft lighting, white walls, warm and cozy atmosphere, home living scene"
    },
    "北欧风": {
        "zh": "北欧风格客厅，白色为主，原木家具，灰色布艺沙发，绿色植物点缀，落地窗，自然光，简洁舒适",
        "en": "Nordic style living room, white as main color, wooden furniture, gray fabric sofa, green plants, floor-to-ceiling windows, natural light, simple and comfortable"
    },
    "日式": {
        "zh": "日式风格客厅，原木家具，低矮沙发，榻榻米元素，藤编收纳，简洁大白墙，自然温馨，禅意氛围",
        "en": "Japanese style living room, wooden furniture, low sofa, tatami elements, rattan storage, simple white walls, natural and warm, Zen atmosphere"
    },
    "新中式": {
        "zh": "新中式客厅，深色实木家具，青花瓷点缀，对称布局，灰色大理石，中国结装饰，典雅大方",
        "en": "New Chinese style living room, dark solid wood furniture, blue and white porcelain elements, symmetrical layout, gray marble, Chinese knot decoration, elegant and generous"
    },
    "意式极简": {
        "zh": "意式极简客厅，黑色皮沙发，黑色茶几，大理石地面，金属装饰，落地窗，高级感，奢华品质",
        "en": "Italian minimalist living room, black leather sofa, black coffee table, marble floor, metal decorations, floor-to-ceiling windows, high-end sense, luxury quality"
    },
    "工业风": {
        "zh": "工业风格客厅，水泥墙面，黑色金属家具，皮质沙发，复古灯具，开放式管线，个性粗犷",
        "en": "Industrial style living room, concrete walls, black metal furniture, leather sofa, vintage lighting, open pipes, personalized and rugged"
    },
    "中古风": {
        "zh": "中古风格客厅，复古家具，柚木色柜子，绿色丝绒沙发，圆形茶几，温暖优雅，怀旧氛围",
        "en": "Mid-century modern living room, vintage furniture, teak cabinets, green velvet sofa, round coffee table, warm and elegant, nostalgic atmosphere"
    }
}

# 预置家具推荐
FURNITURE_RECOMMENDATIONS = {
    "客厅": ["沙发", "茶几", "电视柜", "收纳柜", "落地灯", "地毯", "窗帘"],
    "卧室": ["床", "床垫", "衣柜", "床头柜", "梳妆台", "窗帘", "床品"],
    "餐厅": ["餐桌", "餐椅", "餐边柜", "吊灯"],
    "厨房": ["橱柜", "台面", "五金", "厨房家电"],
    "卫生间": ["浴室柜", "马桶", "花洒", "毛巾架"]
}


@router.post("/generate", response_model=PromptGenerateResponse)
async def generate_prompt(request: PromptGenerateRequest):
    """生成 AI 绘画提示词"""
    try:
        kb = get_knowledge_base()

        # 1. 查找风格信息
        style_results = kb.query(f"{request.style}装修风格", top_k=2)
        style_info = {}
        if style_results:
            style_info = {
                "name": request.style,
                "description": style_results[0].get("content", "")[:300],
                "source": style_results[0].get("source", "")
            }

        # 2. 使用预置模板或生成简单提示词
        template = PROMPT_TEMPLATES.get(request.style)
        if template:
            prompt_zh = f"{request.room_type}，{template['zh']}"
            if request.requirements:
                prompt_zh += f"，{request.requirements}"
            prompt_en = f"{request.room_type}, {template['en']}"
            if request.mood:
                prompt_en += f", {request.mood}"
        else:
            # 简单生成
            prompt_zh = f"{request.style}风格的{request.room_type}，温馨舒适，现代简约，居家氛围"
            prompt_en = f"{request.style} style {request.room_type}, warm and comfortable, modern minimalist, home atmosphere"

        # 3. 推荐家具
        recommended_items = FURNITURE_RECOMMENDATIONS.get(request.room_type, [])

        return PromptGenerateResponse(
            prompt_zh=prompt_zh,
            prompt_en=prompt_en,
            style_info=style_info,
            recommended_items=recommended_items
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))