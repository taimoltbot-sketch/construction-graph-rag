# 測試規則

## 測試覆蓋率

- **目標**：> 80%
- **核心模組**：> 90%
- **新功能**：必須有測試

## TDD 流程

```
1. RED：寫失敗的測試
2. GREEN：寫最少程式碼讓測試通過
3. REFACTOR：重構程式碼
```

## 測試檔案結構

```
tests/
├── __init__.py
├── conftest.py          # pytest fixtures
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_etl.py
├── integration/
│   ├── test_neo4j.py
│   └── test_api.py
└── e2e/
    └── test_rag_pipeline.py
```

## 測試範例

```python
import pytest
from src.rag.query import GraphRAGQuery

@pytest.fixture
def rag_query():
    return GraphRAGQuery()

def test_query_returns_sources(rag_query):
    """測試查詢是否返回來源標註"""
    result = rag_query.query("B1樓層進度")
    
    assert result.answer is not None
    assert result.sources is not None
    assert len(result.sources) > 0

def test_empty_query_handling(rag_query):
    """測試空查詢處理"""
    result = rag_query.query("")
    
    assert result.answer == ""
    assert result.error == "Empty query"
```

## 測試資料

- 使用 Mock Data（不要用生產資料）
- Mock Data 放在 `data/mock_neo4j/` 和 `data/mock_postgres/`
- 確保可重現

## CI/CD 整合

每個 PR 必須：
- [ ] 執行所有測試
- [ ] 覆蓋率報告
- [ ] Lint 檢查
- [ ] 類型檢查（mypy）
