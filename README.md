# Construction Graph RAG

營建業知識圖譜 RAG 系統 - 讓建案相關人員用自然語言查詢 ERP 數據

## 專案結構

```
construction-graph-rag/
├── agents/                 # 子代理定義
│   ├── planner.md          # 任務拆解與進度管理
│   ├── ai-engineer.md      # DSPy、Neo4j、RAG 邏輯
│   ├── backend-engineer.md # ETL Pipeline、PostgreSQL → Neo4j
│   ├── qa-engineer.md      # TDD 測試、Ragas 評估
│   └── code-reviewer.md    # 代碼品質把關
│
├── skills/                 # 工作流定義
│   ├── tdd-workflow/       # TDD 開發流程
│   ├── graph-schema/       # Neo4j Schema 設計
│   ├── etl-pipeline/       # ETL 流程
│   ├── rag-evaluation/     # RAG 評估方法
│   └── dspy-optimization/  # DSPy Prompt 優化
│
├── commands/               # 可執行命令
│   ├── plan.md             # /plan - 規劃任務
│   ├── tdd.md              # /tdd - TDD 開發
│   ├── review.md           # /review - 代碼審查
│   ├── evaluate.md         # /evaluate - 執行評估
│   └── setup-db.md         # /setup-db - 建立資料庫
│
├── rules/                  # 必須遵循的準則
│   ├── security.md         # 資安檢查
│   ├── coding-style.md     # 程式碼風格
│   ├── testing.md          # 測試要求
│   ├── git-workflow.md     # Git 工作流程
│   └── documentation.md    # 文件維護
│
├── src/                    # 程式碼
│   ├── models/             # 資料模型
│   ├── services/           # 服務層
│   ├── etl/                # ETL 程式
│   ├── rag/                # RAG 邏輯
│   ├── api/                # API 端點
│   └── ui/                 # 前端介面
│
├── tests/                  # 測試檔案
├── data/                   # Mock Data
│   ├── mock_neo4j/         # Neo4j Mock Data (Cypher)
│   └── mock_postgres/      # PostgreSQL Mock Data (SQL)
│
├── docs/                   # 文件
├── scripts/                # 腳本工具
├── .env.example            # 環境變數範本
├── CLAUDE.md               # 專案配置
└── README.md               # 說明文件
```

## 核心功能

### 1. 資料層
- PostgreSQL ETL → Neo4j Graph
- Mock Data 生成（營建業 ERP 數據）
- 三元組關係設計

### 2. RAG 層
- Graph RAG Retriever
- Cypher Query 生成
- Source Attribution

### 3. 優化層
- DSPy Prompt 優化
- LangSmith 評估
- Ragas 指標

### 4. 介面層
- 純對話型 Chatbot
- 支援 Markdown + Mermaid 圖表
- Source 標註

## 開發流程

1. **Plan** → 用 `/plan` 規劃任務
2. **TDD** → 用 `/tdd` 開發（先寫測試）
3. **Review** → 用 `/review` 審查代碼
4. **Evaluate** → 用 `/evaluate` 執行評估

## 聯絡方式

Tai's AI Assistant Team 🦫
