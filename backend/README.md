# 装修知识库 API

FastAPI 服务，提供装修知识查询、提示词生成、图像理解能力。

## 环境要求

- Python 3.10-3.12（不支持 Python 3.13+）

## 快速开始

```bash
cd backend

# 检查 Python 版本
python3 --version  # 确保是 3.10-3.12

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python -m uvicorn app.main:app --reload --port 8889
```

## 问题解决

如果遇到 `pydantic-core` 编译错误：

1. **检查 Python 版本**：
   ```bash
   python3 --version
   ```
   需要 Python 3.10-3.12

2. **使用 conda 创建环境**（推荐）：
   ```bash
   conda create -n decor-kb python=3.11
   conda activate decor-kb
   pip install -r requirements.txt
   ```

3. **或者使用系统 Python**（如果版本合适）：
   ```bash
   /usr/bin/python3 --version
   ```

## 测试命令

```bash
# 健康检查
curl http://localhost:8889/health

# 知识查询
curl -X POST http://localhost:8889/api/v1/knowledge/query \
  -H "Content-Type: application/json" \
  -d '{"question": "奶油风有什么特点？"}'
```