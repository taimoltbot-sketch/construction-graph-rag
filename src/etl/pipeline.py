"""
ETL Pipeline: PostgreSQL → Neo4j 三元組轉換
"""

from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
import asyncpg
from neo4j import GraphDatabase

@dataclass
class ETLConfig:
    """ETL 設定"""
    postgres_uri: str
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str

class PostgresExtractor:
    """從 PostgreSQL 提取 ERP 資料"""
    
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.conn: asyncpg.Connection = None
    
    async def connect(self):
        self.conn = await asyncpg.connect(self.dsn)
    
    async def close(self):
        if self.conn:
            await self.conn.close()
    
    async def extract_projects(self) -> List[Dict[str, Any]]:
        """提取建案資料"""
        query = """
        SELECT p.id, p.name, p.status, p.start_date, p.address,
               b.total as budget_total, b.reserved as budget_reserved
        FROM projects p
        LEFT JOIN budgets b ON p.id = b.project_id
        """
        return await self.conn.fetch(query)
    
    async def extract_floors(self) -> List[Dict[str, Any]]:
        """提取樓層資料"""
        query = """
        SELECT f.id, f.project_id, f.floor_name, f.status, f.order_num,
               t.id as task_id, t.name as task_name, t.progress
        FROM floors f
        LEFT JOIN tasks t ON f.id = t.floor_id
        """
        return await self.conn.fetch(query)
    
    async def extract_settlements(self) -> List[Dict[str, Any]]:
        """提取出工結算單"""
        query = """
        SELECT s.id, s.amount, s.date, s.status, s.description,
               t.id as task_id, t.name as task_name
        FROM settlements s
        LEFT JOIN tasks t ON s.task_id = t.id
        """
        return await self.conn.fetch(query)


class Neo4jLoader:
    """將三元組載入 Neo4j"""
    
    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
    
    def connect(self):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
    
    def close(self):
        if self.driver:
            self.driver.close()
    
    def load_triples(self, triples: List[Tuple]):
        """載入三元組"""
        def _create_nodes(tx, triples):
            for triple in triples:
                subject_type, subject_id, predicate, obj = triple
                # 建立 Subject 節點
                tx.run("""
                    MERGE (s:Subject {id: $subject_id, type: $subject_type})
                """, subject_id=subject_id, subject_type=subject_type)
                
                # 建立 Object 值
                tx.run("""
                    MATCH (s:Subject {id: $subject_id, type: $subject_type})
                    SET s.$predicate = $obj
                """, subject_id=subject_id, subject_type=subject_type, predicate=predicate, obj=obj)
        
        with self.driver.session() as session:
            session.execute_write(_create_nodes, triples)
    
    def create_relationships(self, relationships: List[Tuple]):
        """建立關係"""
        def _create_rels(tx, rels):
            for rel in rels:
                from_type, from_id, rel_type, to_type, to_id = rel
                tx.run("""
                    MATCH (from:Subject {id: $from_id, type: $from_type})
                    MATCH (to:Subject {id: $to_id, type: $to_type})
                    MERGE (from)-[:REL {type: $rel_type}]->(to)
                """, from_id=from_id, from_type=from_type, rel_type=rel_type, to_id=to_id, to_type=to_type)
        
        with self.driver.session() as session:
            session.execute_write(_create_rels, relationships)


class Transformer:
    """將資料轉換為三元組"""
    
    @staticmethod
    def project_to_triples(project: Dict) -> List[Tuple]:
        """建案 → 三元組"""
        triples = [
            ("Project", project['id'], "id", project['id']),
            ("Project", project['id'], "name", project['name']),
            ("Project", project['id'], "status", project['status']),
        ]
        if project.get('budget_total'):
            triples.append(("Project", project['id'], "budget_total", project['budget_total']))
        return triples
    
    @staticmethod
    def floor_to_triples(floor: Dict) -> List[Tuple]:
        """樓層 → 三元組"""
        triples = [
            ("Floor", floor['id'], "id", floor['id']),
            ("Floor", floor['id'], "floor_name", floor['floor_name']),
            ("Floor", floor['id'], "status", floor['status']),
        ]
        return triples
    
    @staticmethod
    def settlement_to_triples(settlement: Dict) -> List[Tuple]:
        """結算單 → 三元組"""
        triples = [
            ("Settlement", settlement['id'], "id", settlement['id']),
            ("Settlement", settlement['id'], "amount", str(settlement['amount'])),
            ("Settlement", settlement['id'], "status", settlement['status']),
        ]
        # 可選欄位
        if 'date' in settlement and settlement['date']:
            triples.append(("Settlement", settlement['id'], "date", str(settlement['date'])))
        if 'description' in settlement and settlement['description']:
            triples.append(("Settlement", settlement['id'], "description", settlement['description']))
        return triples


class ETLPipeline:
    """ETL Pipeline 主類別"""
    
    def __init__(self, config: ETLConfig):
        self.config = config
        self.extractor = PostgresExtractor(config.postgres_uri)
        self.loader = Neo4jLoader(config.neo4j_uri, config.neo4j_user, config.neo4j_password)
        self.transformer = Transformer()
    
    async def run(self):
        """執行 ETL"""
        # Connect
        await self.extractor.connect()
        self.loader.connect()
        
        try:
            # Extract
            print("📦 Extracting data from PostgreSQL...")
            projects = await self.extractor.extract_projects()
            floors = await self.extractor.extract_floors()
            settlements = await self.extractor.extract_settlements()
            print(f"   Found {len(projects)} projects, {len(floors)} floors, {len(settlements)} settlements")
            
            # Transform
            print("🔄 Transforming to triples...")
            all_triples = []
            
            for p in projects:
                all_triples.extend(self.transformer.project_to_triples(dict(p)))
            
            for f in floors:
                all_triples.extend(self.transformer.floor_to_triples(dict(f)))
            
            for s in settlements:
                all_triples.extend(self.transformer.settlement_to_triples(dict(s)))
            
            print(f"   Generated {len(all_triples)} triples")
            
            # Load
            print("💾 Loading to Neo4j...")
            self.loader.load_triples(all_triples)
            print("   Done!")
            
        finally:
            await self.extractor.close()
            self.loader.close()


# Mock Data 生成（當沒有 PostgreSQL 時使用）
def generate_mock_triples() -> List[Tuple]:
    """生成營建業 Mock 三元組"""
    triples = []
    
    # 建案
    projects = [
        ("PRJ-001", "台北信義區豪宅", "進行中"),
        ("PRJ-002", "新北市中和住宅", "規劃中"),
    ]
    for pid, name, status in projects:
        triples.append(("Project", pid, "id", pid))
        triples.append(("Project", pid, "name", name))
        triples.append(("Project", pid, "status", status))
    
    # 樓層
    floors = [
        ("F-B1", "B1", "完成"),
        ("F-1F", "1F", "進行中"),
        ("F-2F", "2F", "待施工"),
    ]
    for fid, name, status in floors:
        triples.append(("Floor", fid, "id", fid))
        triples.append(("Floor", fid, "floor_name", name))
        triples.append(("Floor", fid, "status", status))
    
    # 施工項目
    tasks = [
        ("T-001", "鋼筋綁紮", "100"),
        ("T-002", "混凝土澆置", "80"),
        ("T-003", "板模作業", "60"),
    ]
    for tid, name, progress in tasks:
        triples.append(("Task", tid, "id", tid))
        triples.append(("Task", tid, "name", name))
        triples.append(("Task", tid, "progress", progress))
    
    # 結算單
    settlements = [
        ("SET-001", "2500000", "已核准"),
        ("SET-002", "1800000", "審核中"),
    ]
    for sid, amount, status in settlements:
        triples.append(("Settlement", sid, "id", sid))
        triples.append(("Settlement", sid, "amount", amount))
        triples.append(("Settlement", sid, "status", status))
    
    # 關係
    triples.append(("Project", "PRJ-001", "has_floor", "F-B1"))
    triples.append(("Project", "PRJ-001", "has_floor", "F-1F"))
    triples.append(("Floor", "F-B1", "has_task", "T-001"))
    triples.append(("Floor", "F-1F", "has_task", "T-002"))
    triples.append(("Floor", "F-1F", "has_task", "T-003"))
    triples.append(("Task", "T-001", "linked_to", "SET-001"))
    
    return triples


if __name__ == "__main__":
    # 使用 Mock Data 測試
    print("🧪 Generating mock triples...")
    triples = generate_mock_triples()
    print(f"   Generated {len(triples)} triples")
    
    # 印出前 10 個
    print("\n前 10 個三元組:")
    for t in triples[:10]:
        print(f"   ({t[0]}, {t[1]}, {t[2]}, {t[3]})")
