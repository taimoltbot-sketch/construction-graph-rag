# TDD Workflow

## 概述

Test-Driven Development（TDD）工作流程，確保程式碼品質。

## 流程

```
RED → GREEN → REFACTOR
```

### Step 1: RED（紅）
```python
# tests/test_calculator.py
def test_budget_calculation():
    result = calculate_total_cost(
        materials=[{"cost": 1000}],
        labor=[{"cost": 500}]
    )
    assert result == 1500
```

### Step 2: GREEN（綠）
```python
# src/services/calculator.py
def calculate_total_cost(materials, labor):
    # 最少程式碼讓測試通過
    return 1500
```

### Step 3: REFACTOR（重構）
```python
# 重構為正確實作
def calculate_total_cost(materials, labor):
    material_cost = sum(m["cost"] for m in materials)
    labor_cost = sum(l["cost"] for l in labor)
    return material_cost + labor_cost
```

## 原則

1. **一次只做一件事**：每個測試專注一個功能
2. **命名清楚**：測試名稱說明測試什麼
3. **保持簡單**：不要過度設計
4. **紅-綠-重構**：順序不能亂

## 常用指令

```bash
# 執行所有測試
pytest tests/

# 執行單一測試檔案
pytest tests/unit/test_calculator.py

# 執行並顯示覆蓋率
pytest --cov=src tests/

# 監聽檔案變更自動執行
pytest-watch tests/
```

## 檢查清單

- [ ] 每個功能都有測試
- [ ] 測試覆蓋率 > 80%
- [ ] 測試可獨立執行
- [ ] 測試穩定（不隨機失敗）
- [ ] 測試速度快（< 1 秒）
