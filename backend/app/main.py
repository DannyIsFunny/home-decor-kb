"""
Home Decor Knowledge Base API
装修知识库 API 服务
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.api import knowledge, prompt, image

# 加载环境变量
load_dotenv()

# 检查 API Key
if not os.getenv("MINIMAX_API_KEY"):
    # 使用用户提供的 key
    os.environ["MINIMAX_API_KEY"] = "sk-cp-DQWg6T6LVx2S7smjIwD-8C5jyLEKBNYmI_YqVtGNYuLdsXJmogQM_2Si11xPfjBZ5sTFcK-qdJmUY374oPeiV5BsXgGZ-kPXFedqb0yaUo7oH9T7fwxpmJc"

app = FastAPI(
    title="Home Decor Knowledge Base API",
    description="装修知识库 API，提供知识查询、提示词生成、图像理解能力",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(knowledge.router, prefix="/api/v1")
app.include_router(prompt.router, prefix="/api/v1")
app.include_router(image.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "name": "Home Decor Knowledge Base API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "home-decor-kb"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8889)