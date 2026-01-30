# 程式碼風格規則

## 命名規範

### 變數與函數
```python
# ✅ Good
project_name = "台北豪宅"
def calculate_budget(): ...

# ❌ Bad
p = "台北豪宅"
def calc(): ...
```

### 類別
```python
# ✅ Good
class Neo4jClient: ...
class BudgetCalculator: ...

# ❌ Bad
class neo4j: ...
class budget: ...
```

### 常數
```python
# ✅ Good
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# ❌ Bad
maxRetries = 3
default_timeout = 30
```

## 函數設計

- 職責單一（SRP）
- 簡短為佳（< 50 行）
- 輸入輸出清晰
- 使用 type hints

```python
def calculate_floor_cost(
    floor_id: str,
    tasks: list[Task],
    materials: list[Material]
) -> float:
    """計算樓層施工成本
    
    Args:
        floor_id: 樓層 ID
        tasks: 施工項目清單
        materials: 材料清單
    
    Returns:
        總成本金額
    """
    total = sum(t.cost for t in tasks)
    total += sum(m.cost for m in materials)
    return total
```

## 檔案組織

- 每個檔案 < 500 行
- 相關功能放同一檔案
- 使用 `__init__.py` 組織 package

## 註解規範

- 說明「為什麼」，而非「是什麼」
- 複雜邏輯必須註解
- 使用 docstring

```python
# ❌ Bad - 廢話註解
# 增加 i
i += 1

# ✅ Good - 說明原因
# 索引遞增，處理下一筆資料
i += 1
```
