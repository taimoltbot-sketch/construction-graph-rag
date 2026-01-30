# Git 工作流程

## Branch 命名

| 類型 | 範例 |
|-----|------|
| Feature | `feature/etl-pipeline` |
| Bug Fix | `bugfix/fix-neo4j-connection` |
| Hotfix | `hotfix/security-patch` |
| Refactor | `refactor/improve-rag-retriever` |

## Commit 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type
- `feat`: 新功能
- `fix`: 修復 bug
- `docs`: 文件更新
- `style`: 程式碼格式
- `refactor`: 重構
- `test`: 測試
- `chore`: 維護工作

### 範例

```
feat(etl): 新增 PostgreSQL 到 Neo4j 轉換功能

- 支援建案資料轉換
- 支援預算資料轉換
- 新增批次處理

Closes #12
```

## Pull Request

### PR 標題
```
[<type>] <簡短描述>
```

### PR 內容
1. **描述**：做了什麼
2. **測試**：如何驗證
3. **截圖**（如有 UI 變更）

### Review 要求
- 至少 1 人 Review
- Code Reviewer 批准
- 測試通過

## Tag 格式

```
v<major>.<minor>.<patch>
```

範例：`v1.0.0`, `v1.1.0`, `v1.1.1`
