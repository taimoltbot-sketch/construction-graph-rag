# Construction Graph RAG - Project Configuration

## 專案概述

營建業知識圖譜 RAG 系統，讓建案相關人員用自然語言查詢 ERP 數據。

## 模型設定

- **Default Model**: `minimax/MiniMax-M2.1`
- **Thinking**: off（預設）

## 環境變數

建立 `.env` 檔案（不要 Commit）：

```bash
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# PostgreSQL
POSTGRES_URI=postgresql://user:password@localhost:5432/erp_db

# OpenAI（DSPy 使用）
OPENAI_API_KEY=sk-...

# LangSmith（評估追蹤）
LANGSMITH_API_KEY=ls_...
LANGSMITH_TRACING=true
```

## Agents 配置

此專案使用以下子代理：

- `planner.md` - 任務拆解與規劃
- `ai-engineer.md` - AI/RAG/DSPy 實作
- `backend-engineer.md` - ETL Pipeline
- `qa-engineer.md` - 測試與評估
- `code-reviewer.md` - 代碼審查

## Rules

此專案遵守以下規則：

- `security.md` - 資安檢查
- `coding-style.md` - 程式碼風格
- `testing.md` - 測試要求
- `git-workflow.md` - Git 工作流程

## MCP Servers

建議啟用：
- `postgres` - PostgreSQL 連接
- `neo4j` - Neo4j 連接

## Commands

可用命令：
- `/plan` - 規劃任務
- `/tdd` - TDD 開發
- `/review` - 代碼審查
- `/evaluate` - 執行評估

## 專案結構

```
construction-graph-rag/
├── agents/          # 子代理定義
├── skills/          # 工作流定義
├── commands/        # 可執行命令
├── rules/           # 必須遵循的準則
├── src/             # 程式碼
├── tests/           # 測試
├── data/            # Mock Data
├── docs/            # 文件
└── scripts/         # 腳本
```

## 開發流程

1. 用 `/plan` 規劃任務
2. 用 `/tdd` 開發功能
3. 用 `/review` 審查代碼
4. 用 `/evaluate` 評估品質
