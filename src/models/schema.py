"""Neo4j Graph Schema for Construction Domain"""

# Node Labels
NODE_LABELS = {
    "Project": "建案",
    "Budget": "預算",
    "Contract": "統包合約",
    "Settlement": "出工結算單",
    "CashFlow": "出工出料資金流量表",
    "CostEstimate": "成本估算",
    "ActualCost": "實際運行成本",
    "AdditionalCost": "工料追加成本",
    "Floor": "樓層",
    "Task": "施工項目",
    "Material": "材料",
    "Labor": "工班",
    "Supplier": "供應商",
}

# Relationship Types
RELATIONSHIPS = {
    "OWNS": "建案 -> 擁有 -> 預算/合約/資金流",
    "HAS_FLOOR": "建案 -> 包含 -> 樓層",
    "FLOOR_HAS_TASK": "樓層 -> 執行 -> 施工項目",
    "TASK_NEEDS_MATERIAL": "施工項目 -> 需要 -> 材料",
    "TASK_NEEDS_LABOR": "施工項目 -> 需要 -> 工班",
    "TASK_LINKED_TO_SETTLEMENT": "施工項目 -> 對應 -> 結算單",
    "COST_BREAKDOWN": "預算 -> 細分 -> 實際成本",
    "ADDITIONAL_COST": "成本 -> 追加 -> 工料追加",
    "CASH_FLOW": "資金 -> 流向 -> 各項目",
    "SUPPLIES": "供應商 -> 供應 -> 材料",
}

# Schema Definition
SCHEMA = """
Node Types:
- Project: id, name, status, start_date, end_date, address
- Budget: id, type, total, reserved, spent, currency
- Contract: id, name, amount, sign_date, contractor
- Settlement: id, amount, date, status, description
- Floor: id, floor_name, status, order
- Task: id, name, progress, unit, unit_price
- Material: id, name, spec, unit, unit_price
- Labor: id, name, type, daily_rate
- Supplier: id, name, contact, phone, address

Relationships:
- (Project)-[:OWNS]->(Budget)
- (Project)-[:HAS_FLOOR]->(Floor)
- (Project)-[:HAS_CONTRACT]->(Contract)
- (Floor)-[:HAS_TASK]->(Task)
- (Task)-[:NEEDS_MATERIAL]->(Material)
- (Task)-[:NEEDS_LABOR]->(Labor)
- (Task)-[:LINKED_TO]->(Settlement)
- (Budget)-[:COVERS]->(ActualCost)
- (ActualCost)-[:ADDS_TO]->(AdditionalCost)
- (Supplier)-[:SUPPLIES]->(Material)
"""

# Cypher Constraints
CONSTRAINTS = """
CREATE CONSTRAINT project_id IF NOT EXISTS ON (p:Project) ASSERT p.id IS UNIQUE;
CREATE CONSTRAINT budget_id IF NOT EXISTS ON (b:Budget) ASSERT b.id IS UNIQUE;
CREATE CONSTRAINT contract_id IF NOT EXISTS ON (c:Contract) ASSERT c.id IS UNIQUE;
CREATE CONSTRAINT settlement_id IF NOT EXISTS ON (s:Settlement) ASSERT s.id IS UNIQUE;
CREATE CONSTRAINT floor_id IF NOT EXISTS ON (f:Floor) ASSERT f.id IS UNIQUE;
CREATE CONSTRAINT task_id IF NOT EXISTS ON (t:Task) ASSERT t.id IS UNIQUE;
"""
