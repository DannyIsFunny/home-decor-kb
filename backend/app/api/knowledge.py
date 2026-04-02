"""
知识查询 API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from app.core.knowledge_base import get_knowledge_base

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


class QueryRequest(BaseModel):
    """知识查询请求"""
    question: str
    top_k: Optional[int] = 5
    use_llm: Optional[bool] = False  # 默认不使用 LLM，直接返回检索结果


class QueryResponse(BaseModel):
    """知识查询响应"""
    answer: str
    references: List[Dict[str, Any]]


@router.get("/categories")
async def list_categories():
    """获取知识分类列表"""
    kb = get_knowledge_base()
    return {
        "categories": kb.get_categories()
    }


@router.get("/categories/{category}")
async def query_by_category(category: str, limit: int = 10):
    """按分类查询知识"""
    kb = get_knowledge_base()
    results = kb.query_by_category(category, limit)
    return {
        "category": category,
        "count": len(results),
        "results": results
    }


@router.post("/query", response_model=QueryResponse)
async def query_knowledge(request: QueryRequest):
    """语义检索知识"""
    try:
        kb = get_knowledge_base()

        # 语义检索
        references = kb.query(request.question, request.top_k or 5)

        if not references:
            return QueryResponse(
                answer="抱歉，知识库中暂时没有找到相关内容。",
                references=[]
            )

        # 直接返回检索结果
        answer = "以下是从知识库中找到的相关内容：\n\n"
        for i, ref in enumerate(references[:3], 1):
            answer += f"{i}. 【{ref['source']}】{ref['content'][:300]}...\n\n"

        return QueryResponse(
            answer=answer,
            references=references
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))