"""Mock Data for Neo4j - Construction Domain"""

MOCK_DATA_CYPHER = """
// Create Projects
CREATE (:Project {id: "PRJ-001", name: "台北信義區豪宅", status: "進行中", start_date: "2024-01-01", address: "台北市信義區"})
CREATE (:Project {id: "PRJ-002", name: "新北市中和住宅", status: "規劃中", start_date: "2024-06-01", address: "新北市中和區"})

// Create Budgets
CREATE (:Budget {id: "B-001", type: "建案預算", total: 500000000, reserved: 480000000, spent: 120000000, currency: "TWD"})
CREATE (:Budget {id: "B-002", type: "土地開發預算", total: 800000000, reserved: 800000000, spent: 0, currency: "TWD"})

// Create Floors
CREATE (:Floor {id: "F-B1", floor_name: "B1", status: "完成", order: 0})
CREATE (:Floor {id: "F-1F", floor_name: "1F", status: "進行中", order: 1})
CREATE (:Floor {id: "F-2F", floor_name: "2F", status: "待施工", order: 2})

// Create Tasks
CREATE (:Task {id: "T-001", name: "鋼筋綁紮", progress: 100, unit: "噸", unit_price: 25000})
CREATE (:Task {id: "T-002", name: "混凝土澆置", progress: 80, unit: "立方公尺", unit_price: 3000})
CREATE (:Task {id: "T-003", name: "板模作業", progress: 60, unit: "平方公尺", unit_price: 4500})
CREATE (:Task {id: "T-004", name: "水電配置", progress: 30, unit: "公尺", unit_price: 800})

// Create Materials
CREATE (:Material {id: "M-001", name: "鋼筋", spec: "#10", unit: "噸", unit_price: 25000})
CREATE (:Material {id: "M-002", name: "混凝土", spec: "4000psi", unit: "立方公尺", unit_price: 3000})
CREATE (:Material {id: "M-003", name: "模板", spec: "柳安木", unit: "平方公尺", unit_price: 450})

// Create Settlements
CREATE (:Settlement {id: "SET-001", amount: 2500000, date: "2024-12-15", status: "已核准", description: "B1鋼筋綁紮"})
CREATE (:Settlement {id: "SET-002", amount: 1800000, date: "2024-12-20", status: "審核中", description: "1F混凝土澆置"})

// Create Relationships
MATCH (p:Project {id: "PRJ-001"})
MATCH (b:Budget {id: "B-001"})
CREATE (p)-[:OWNS {budget_type: "建案預算"}]->(b)

MATCH (p:Project {id: "PRJ-001"})
MATCH (f:Floor {id: "F-B1"})
CREATE (p)-[:HAS_FLOOR]->(f)

MATCH (f:Floor {id: "F-B1"})
MATCH (t:Task {id: "T-001"})
CREATE (f)-[:HAS_TASK {progress: 100}]->(t)

MATCH (t:Task {id: "T-001"})
MATCH (m:Material {id: "M-001"})
CREATE (t)-[:NEEDS_MATERIAL {quantity: 100, unit: "噸"}]->(m)

MATCH (t:Task {id: "T-001"})
MATCH (s:Settlement {id: "SET-001"})
CREATE (t)-[:LINKED_TO {amount: 2500000}]->(s)
"""

# Example Questions for Evaluation
MOCK_QUESTIONS = [
    {
        "question": "B1樓層的鋼筋作業完成度多少？",
        "expected_answer": "B1鋼筋作業已完成100%",
        "expected_cypher": "MATCH (f:Floor {floor_name: 'B1'})-[:HAS_TASK]->(t:Task {name: '鋼筋綁紮'}) RETURN t.progress"
    },
    {
        "question": "鋼筋綁紮用了多少材料和成本？",
        "expected_answer": "鋼筋綁紮使用了100噸鋼筋，總成本2,500,000元",
        "expected_cypher": "MATCH (t:Task {name: '鋼筋綁紮'})-[:NEEDS_MATERIAL]->(m:Material) RETURN m.name, m.spec, t.unit_price * 100 as total_cost"
    },
    {
        "question": "建案目前的預算執行狀況？",
        "expected_answer": "建案預算5億，已執行1.2億，執行率24%",
        "expected_cypher": "MATCH (p:Project)-[:OWNS]->(b:Budget {type: '建案預算'}) RETURN b.total, b.spent, b.spent * 100.0 / b.total as execution_rate"
    },
]
