# ETL Pipeline

## 資料流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ PostgreSQL  │ ──→ │   Transform │ ──→ │    Neo4j    │
│ (ERP Data)  │     │ (Triples)   │     │   (Graph)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Step 1: Extract（提取）

```python
# src/etl/extract.py
from src.db.postgres import PostgresClient

async def extract_projects() -> List[dict]:
    """從 PostgreSQL 提取建案資料"""
    query = """
    SELECT p.id, p.name, p.status, p.start_date,
           b.total as budget_total, b.reserved as budget_reserved
    FROM projects p
    LEFT JOIN budgets b ON p.id = b.project_id
    """
    return await PostgresClient.fetchall(query)

async def extract_floors() -> List[dict]:
    """提取樓層資料"""
    query = """
    SELECT f.id, f.project_id, f.floor_name, f.status,
           t.id as task_id, t.name as task_name, t.progress
    FROM floors f
    LEFT JOIN tasks t ON f.id = t.floor_id
    """
    return await PostgresClient.fetchall(query)
```

## Step 2: Transform（轉換）

```python
# src/etl/transform.py
from typing import List, Tuple

def project_to_triples(project: dict) -> List[Tuple]:
    """將建案轉換為三元組"""
    triples = [
        ("Project", project["id"], "id", project["id"]),
        ("Project", project["id"], "name", project["name"]),
        ("Project", project["id"], "status", project["status"]),
    ]
    if project.get("budget_total"):
        triples.append(("Project", project["id"], "has_budget_total", project["budget_total"]))
    return triples

def task_to_triples(task: dict) -> List[Tuple]:
    """將施工項目轉換為三元組"""
    return [
        ("Task", task["id"], "name", task["name"]),
        ("Task", task["id"], "progress", task["progress"]),
        ("Floor", task["floor_id"], "has_task", task["id"]),
    ]
```

## Step 3: Load（載入）

```python
# src/etl/load.py
from src.db.neo4j import Neo4jClient

async def load_triples(triples: List[Tuple]):
    """將三元組載入 Neo4j"""
    cypher = """
    UNWIND $triples AS t
    MERGE (s:Subject {id: t[1]})
    SET s += CASE WHEN t[2] = 'id' THEN {} ELSE {property: t[2], value: t[3]} END
    """
    await Neo4jClient.execute(cypher, {"triples": triples})
```

## 執行 Pipeline

```bash
# 執行完整 ETL
python -m src.etl.main

# 只執行 Extract
python -m src.etl.extract

# 從指定時間點繼續
python -m src.etl.main --from 2024-01-01
```
