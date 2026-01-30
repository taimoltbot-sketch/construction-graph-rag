# /tdd - Test-Driven Development

## 使用方式

```
/tdd <功能描述>
```

## 功能

1. 先寫測試
2. 實作功能
3. 重構程式碼

## TDD 流程

```
RED (紅) → GREEN (綠) → REFACTOR (重構)
1. 寫失敗的測試
2. 寫最少程式碼讓測試通過
3. 重構程式碼
```

## 範例

```
/tdd 建立 Neo4j 連接模組
```

## 產出

```python
# tests/test_neo4j.py
import pytest

def test_neo4j_connection():
    from src.services.neo4j import Neo4jClient
    client = Neo4jClient()
    assert client.connect() == True

# src/services/neo4j.py (最小實作)
class Neo4jClient:
    def connect(self):
        return True
```
