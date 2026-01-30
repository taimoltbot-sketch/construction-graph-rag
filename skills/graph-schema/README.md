# Neo4j Graph Schema

## 營建業資料模型

### Node Types

```cypher
CREATE CONSTRAINT project_id ON (p:Project) ASSERT p.id IS UNIQUE;
CREATE CONSTRAINT budget_id ON (b:Budget) ASSERT b.id IS UNIQUE;
CREATE CONSTRAINT contract_id ON (c:Contract) ASSERT c.id IS UNIQUE;
```

### 節點定義

| 標籤 | 說明 | 屬性 |
|-----|------|------|
| `Project` | 建案 | id, name, status, start_date, end_date |
| `Budget` | 預算 | id, type, total, reserved, spent |
| `Contract` | 統包合約 | id, name, amount, sign_date |
| `Settlement` | 出工結算單 | id, amount, date, status |
| `Floor` | 樓層 | id, floor_name, status |
| `Task` | 施工項目 | id, name, progress, unit |
| `Material` | 材料 | id, name, spec, unit_price |
| `Labor` | 工班 | id, name, type |
| `Supplier` | 供應商 | id, name, contact |

### Relationship Types

```cypher
(:Project)-[:OWNS]->(:Budget)
(:Project)-[:HAS_FLOOR]->(:Floor)
(:Project)-[:HAS_CONTRACT]->(:Contract)
(:Floor)-[:HAS_TASK]->(:Task)
(:Task)-[:NEEDS_MATERIAL]->(:Material)
(:Task)-[:NEEDS_LABOR]->(:Labor)
(:Task)-[:LINKED_TO]->(:Settlement)
(:Budget)-[:COVERS]->(:Cost)
(:Cost)-[:ADDS_TO]->(:AdditionalCost)
```

### Mock Data 範例

```cypher
// 建案
CREATE (:Project {id: "PRJ-001", name: "台北信義豪宅", status: "進行中"})
CREATE (:Budget {id: "B-001", type: "建案預算", total: 500000000})
CREATE (:Floor {id: "F-B1", floor_name: "B1", status: "完成"})
CREATE (:Floor {id: "F-1F", floor_name: "1F", status: "進行中"})

// 關係
MATCH (p:Project {id: "PRJ-001"})
MATCH (b:Budget {id: "B-001"})
CREATE (p)-[:OWNS {budget_type: "建案預算"}]->(b)

MATCH (f:Floor {id: "F-B1"})
MATCH (t:Task {id: "T-001"})
CREATE (f)-[:HAS_TASK {progress: 100}]->(t)
```
