"""
Mock Data 生成腳本 - 營建業 ERP 數據
"""

# Mock Data 模板
MOCK_PROJECTS = [
    {
        "id": "PRJ-001",
        "name": "台北信義區豪宅",
        "status": "進行中",
        "start_date": "2024-01-01",
        "address": "台北市信義區信義路五段",
        "budget_total": 500000000,
        "budget_reserved": 480000000,
    },
    {
        "id": "PRJ-002",
        "name": "新北市中和住宅",
        "status": "規劃中",
        "start_date": "2024-06-01",
        "address": "新北市中和區建一路",
        "budget_total": 350000000,
        "budget_reserved": 350000000,
    },
]

MOCK_BUDGETS = [
    {"id": "B-001", "project_id": "PRJ-001", "type": "建案預算", "total": 500000000, "reserved": 480000000, "spent": 120000000},
    {"id": "B-002", "project_id": "PRJ-001", "type": "土地開發預算", "total": 800000000, "reserved": 800000000, "spent": 0},
    {"id": "B-003", "project_id": "PRJ-002", "type": "建案預算", "total": 350000000, "reserved": 350000000, "spent": 0},
]

MOCK_FLOORS = [
    {"id": "F-B1", "project_id": "PRJ-001", "floor_name": "B1", "status": "完成", "order_num": 0},
    {"id": "F-1F", "project_id": "PRJ-001", "floor_name": "1F", "status": "進行中", "order_num": 1},
    {"id": "F-2F", "project_id": "PRJ-001", "floor_name": "2F", "status": "待施工", "order_num": 2},
]

MOCK_TASKS = [
    {"id": "T-001", "floor_id": "F-B1", "name": "鋼筋綁紮", "progress": 100, "unit": "噸", "unit_price": 25000},
    {"id": "T-002", "floor_id": "F-1F", "name": "混凝土澆置", "progress": 80, "unit": "立方公尺", "unit_price": 3000},
    {"id": "T-003", "floor_id": "F-1F", "name": "板模作業", "progress": 60, "unit": "平方公尺", "unit_price": 4500},
]

MOCK_SETTLEMENTS = [
    {"id": "SET-001", "task_id": "T-001", "amount": 2500000, "date": "2024-12-15", "status": "已核准", "description": "B1鋼筋綁紮"},
    {"id": "SET-002", "task_id": "T-002", "amount": 1800000, "date": "2024-12-20", "status": "審核中", "description": "1F混凝土澆置"},
]


def generate_sql_insert():
    """生成 PostgreSQL INSERT 語句"""
    sql_lines = []
    sql_lines.append("-- Mock Data for PostgreSQL")
    sql_lines.append("")
    
    sql_lines.append("-- Projects")
    for p in MOCK_PROJECTS:
        sql = f"INSERT INTO projects (id, name, status, start_date, address, budget_total, budget_reserved) "
        sql += f"VALUES ('{p['id']}', '{p['name']}', '{p['status']}', '{p['start_date']}', '{p['address']}', {p['budget_total']}, {p['budget_reserved']});"
        sql_lines.append(sql)
    
    sql_lines.append("")
    sql_lines.append("-- Budgets")
    for b in MOCK_BUDGETS:
        sql = f"INSERT INTO budgets (id, project_id, type, total, reserved, spent) "
        sql += f"VALUES ('{b['id']}', '{b['project_id']}', '{b['type']}', {b['total']}, {b['reserved']}, {b['spent']});"
        sql_lines.append(sql)
    
    sql_lines.append("")
    sql_lines.append("-- Floors")
    for f in MOCK_FLOORS:
        sql = f"INSERT INTO floors (id, project_id, floor_name, status, order_num) "
        sql += f"VALUES ('{f['id']}', '{f['project_id']}', '{f['floor_name']}', '{f['status']}', {f['order_num']});"
        sql_lines.append(sql)
    
    sql_lines.append("")
    sql_lines.append("-- Tasks")
    for t in MOCK_TASKS:
        sql = f"INSERT INTO tasks (id, floor_id, name, progress, unit, unit_price) "
        sql += f"VALUES ('{t['id']}', '{t['floor_id']}', '{t['name']}', {t['progress']}, '{t['unit']}', {t['unit_price']});"
        sql_lines.append(sql)
    
    return "\n".join(sql_lines)


def generate_cypher_create():
    """生成 Neo4j CREATE 語句"""
    cypher_lines = []
    cypher_lines.append("-- Neo4j Mock Data")
    cypher_lines.append("")
    
    for p in MOCK_PROJECTS:
        cypher = f"CREATE (:Project {{id: '{p['id']}', name: '{p['name']}', status: '{p['status']}'}});"
        cypher_lines.append(cypher)
    
    for b in MOCK_BUDGETS:
        cypher = f"CREATE (:Budget {{id: '{b['id']}', type: '{b['type']}', total: {b['total']}, spent: {b['spent']}}});"
        cypher_lines.append(cypher)
    
    for f in MOCK_FLOORS:
        cypher = f"CREATE (:Floor {{id: '{f['id']}', floor_name: '{f['floor_name']}', status: '{f['status']}'}});"
        cypher_lines.append(cypher)
    
    for t in MOCK_TASKS:
        cypher = f"CREATE (:Task {{id: '{t['id']}', name: '{t['name']}', progress: {t['progress']}}});"
        cypher_lines.append(cypher)
    
    for s in MOCK_SETTLEMENTS:
        cypher = f"CREATE (:Settlement {{id: '{s['id']}', amount: {s['amount']}, status: '{s['status']}'}});"
        cypher_lines.append(cypher)
    
    cypher_lines.append("")
    cypher_lines.append("-- Relationships")
    cypher_lines.append("MATCH (p:Project {id: 'PRJ-001'}), (b:Budget {id: 'B-001'}) CREATE (p)-[:OWNS]->(b);")
    cypher_lines.append("MATCH (p:Project {id: 'PRJ-001'}), (f:Floor {id: 'F-B1'}) CREATE (p)-[:HAS_FLOOR]->(f);")
    cypher_lines.append("MATCH (f:Floor {id: 'F-B1'}), (t:Task {id: 'T-001'}) CREATE (f)-[:HAS_TASK]->(t);")
    cypher_lines.append("MATCH (t:Task {id: 'T-001'}), (s:Settlement {id: 'SET-001'}) CREATE (t)-[:LINKED_TO]->(s);")
    
    return "\n".join(cypher_lines)


if __name__ == "__main__":
    print("=" * 60)
    print("Mock Data Generator - Construction ERP")
    print("=" * 60)
    print()
    
    print("=== PostgreSQL INSERT Statements ===")
    print(generate_sql_insert())
    
    print()
    print("=" * 60)
    print()
    
    print("=== Neo4j CREATE Statements ===")
    print(generate_cypher_create())
