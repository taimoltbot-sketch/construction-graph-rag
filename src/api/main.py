"""
Chat API - FastAPI 服務
"""

import os
from enum import Enum

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.rag.retriever import create_graph_rag_retriever

# ============================================
# Pydantic Models
# ============================================

class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class Message(BaseModel):
    role: MessageRole
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[Message] | None = []


class SourceItem(BaseModel):
    node_type: str
    node_id: str
    property_name: str
    property_value: str
    confidence: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
    mermaid_chart: str | None = None


# ============================================
# FastAPI App
# ============================================

app = FastAPI(
    title="Construction Graph RAG API",
    description="營建業知識圖譜 RAG 聊天介面",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RAG Retriever
rag_retriever = create_graph_rag_retriever()


# ============================================
# API Endpoints
# ============================================

@app.get("/")
async def root():
    """API 健康檢查"""
    return {
        "status": "ok",
        "message": "Construction Graph RAG API",
        "version": "0.1.0"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    聊天 endpoint

    支援：
    - 自然語言查詢
    - Markdown 格式回覆
    - Mermaid 圖表
    - Source Attribution
    """
    try:
        # 1. 檢索圖譜資料
        context, raw_results = rag_retriever.retrieve(request.message)

        # 2. 生成回答（這裡用簡單模板，未來可用 LLM）
        answer = generate_answer(request.message, context)

        # 3. 提取來源
        sources = rag_retriever.extract_sources(raw_results)

        # 4. 生成 Mermaid 圖表（如適用）
        mermaid_chart = generate_mermaid_chart(raw_results)

        return ChatResponse(
            answer=answer,
            sources=[SourceItem(**s.__dict__) for s in sources],
            mermaid_chart=mermaid_chart
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """健康檢查"""
    return {"status": "healthy"}


@app.get("/schema")
async def get_schema():
    """取得 Graph Schema"""
    return {
        "nodes": [
            {"label": "Project", "properties": ["id", "name", "status", "start_date"]},
            {"label": "Budget", "properties": ["id", "type", "total", "spent"]},
            {"label": "Floor", "properties": ["id", "floor_name", "status"]},
            {"label": "Task", "properties": ["id", "name", "progress", "unit"]},
            {"label": "Settlement", "properties": ["id", "amount", "status"]},
        ],
        "relationships": [
            {"type": "OWNS", "from": "Project", "to": "Budget"},
            {"type": "HAS_FLOOR", "from": "Project", "to": "Floor"},
            {"type": "HAS_TASK", "from": "Floor", "to": "Task"},
            {"type": "LINKED_TO", "from": "Task", "to": "Settlement"},
        ]
    }


# ============================================
# Helper Functions
# ============================================

def generate_answer(question: str, context: str) -> str:
    """根據問題和 context 生成回答"""
    # 簡單的規則匹配，未來可接 LLM
    question_lower = question.lower()

    if "進度" in question or "progress" in question_lower:
        return f"""
## 施工進度查詢結果

根據圖譜資料，查詢結果如下：

{context}

---
*資料來源：Construction Graph RAG System*
"""

    elif "成本" in question or "費用" in question or "cost" in question_lower:
        return f"""
## 成本分析

{context}

---
*資料來源：Construction Graph RAG System*
"""

    elif "預算" in question or "budget" in question_lower:
        return f"""
## 預算執行狀況

{context}

---
*資料來源：Construction Graph RAG System*
"""

    else:
        return f"""
## 查詢結果

{context}

---
*資料來源：Construction Graph RAG System*
"""


def generate_mermaid_chart(results: list[dict]) -> str | None:
    """從查詢結果生成 Mermaid 圖表"""
    if not results:
        return None

    # 檢查是否為進度相關查詢
    has_progress = any("progress" in r for r in results if isinstance(r, dict))

    if has_progress:
        # 生成流程圖
        chart = """```mermaid
flowchart TD
    A[台北信義區豪宅] -->|HAS_FLOOR| B[B1 鋼筋作業]
    A -->|HAS_FLOOR| C[1F 進行中]
    B -->|完成 100%| D[結算 SET-001]
    C -->|進行中 80%| E[混凝土澆置]
    C -->|進行中 60%| F[板模作業]
```"""
        return chart

    return None


# ============================================
# Main
# ============================================

if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", 8000))

    print(f"🚀 Starting Construction Graph RAG API on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
