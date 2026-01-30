# Git 工作流程（嚴格版）

## Branch 命名規範

| 類型 | 範例 | 說明 |
|-----|------|------|
| Feature | `feature/etl-pipeline` | 新功能 |
| Bugfix | `bugfix/fix-data-loss` | 修復 bug |
| Hotfix | `hotfix/security-patch` | 緊急修復 |
| Refactor | `refactor/improve-retriever` | 重構 |
| Chore | `chore/update-dependencies` | 維護工作 |

## Commit 格式（Conventional Commits）

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 類型
- `feat`: 新功能
- `fix`: 修復 bug
- `docs`: 文件更新
- `style`: 程式碼格式
- `refactor`: 重構
- `test`: 測試
- `chore`: 維護工作

### 範例
```
feat(etl): 新增 PostgreSQL 連接模組

- 新增 PostgresClient 類別
- 實作 async fetch 方法
- 新增連接池管理

Closes #123
```

## TDD 開發流程（強制）

每個功能必須遵循：

```
1. 📝 Write Test (RED)     → 寫測試，預期失敗
2. 💻 Write Code (GREEN)   → 寫最少程式碼讓測試通過
3. ♻️  Refactor (IMPROVE)  → 重構程式碼
4. ✅ Commit & Push        → 提交變更
5. 🔀 Open PR              → 開 Pull Request
6. 👀 Code Review          → 至少 1 人 review
7. ✅ Merge                → 合併到 main
```

### TDD 範例：ETL Pipeline

```bash
# 1. 建立 branch
git checkout -b feature/etl-pipeline

# 2. RED - 寫測試
# tests/test_etl_pipeline.py
def test_extract_projects():
    """測試資料提取"""
    assert extract_projects() == [...]

# 3. GREEN - 寫功能
# src/etl/pipeline.py
def extract_projects():
    return []  # 最少程式碼

# 4. IMPROVE - 重構
# 完成真正的實作

# 5. Commit
git add tests/ src/
git commit -m "feat(etl): 新增資料提取功能

- 新增 extract_projects 函數
- 新增 extract_floors 函數
- 新增 extract_settlements 函數

Closes #1"

# 6. Push & PR
git push origin feature/etl-pipeline
# → 在 GitHub 開 PR
```

## PR 流程

### PR 標題
```
[<type>] <簡短描述>

範例：
[feat] 新增 ETL Pipeline 功能
[fix] 修復資料遺漏問題
[refactor] 重構 RAG Retriever
```

### PR 描述模板
```markdown
## 功能描述
<!-- 描述做了什麼 -->

## 測試結果
<!-- 測試截圖或結果 -->

## 變更項目
<!-- 列出所有變更 -->

## 相關 Issue
<!-- Closes #123 -->
```

### Review 要求
- ✅ 至少 1 人批准
- ✅ 所有 CI/CD 測試通過
- ✅ 測試覆蓋率 > 80%

## Git Flow 示意

```
main (保護分支)
  │
  ├── feature/etl-pipeline
  │     ├── commit: 新增 extract 測試
  │     ├── commit: 新增 extract 功能
  │     └── commit: 重構並完成 ETL
  │           ↓
  └─► Pull Request → Review → Merge
```

## 每個 Commit 的要求

1. **原子性**：每次 commit 做一件事
2. **可測試**：每個功能都有對應測試
3. **可回滾**：commit 後系統仍可正常運行

## 禁止事項

- ❌ 直接 commit 到 main
- ❌ 合併未測試的程式碼
- ❌ 大型 commit（一次改太多）
- ❌ 空的 commit message
