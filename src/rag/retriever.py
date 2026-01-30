"""
Graph RAG Retriever - Neo4j 圖譜搜尋
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from neo4j import GraphDatabase
import os


@dataclass
class Source:
    """來源標註"""
    node_type: str
    node_id: str
    property_name: str
    property_value: str
    confidence: float = 1.0


@dataclass
class RAGResult:
    """RAG 查詢結果"""
    answer: str
    sources: List[Source]
    cypher_query: str
    raw_results: List[Dict]


class Neo4jGraphClient:
    """Neo4j 客戶端"""
    
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
    
    def query(self, cypher: str, parameters: dict = None) -> List[Dict]:
        """執行 Cypher 查詢"""
        with self.driver.session() as session:
            result = session.run(cypher, parameters)
            return [dict(record) for record in result]
    
    def get_schema(self) -> str:
        """取得 Graph Schema"""
        schema = """
Node Types:
- Project: id, name, status, start_date, address, budget_total
- Budget: id, type, total, reserved, spent
- Floor: id, floor_name, status, order_num
- Task: id, name, progress, unit, unit_price
- Settlement: id, amount, date, status, description
- Material: id, name, spec, unit, unit_price

Relationships:
- (Project)-[:OWNS]->(Budget)
- (Project)-[:HAS_FLOOR]->(Floor)
- (Floor)-[:HAS_TASK]->(Task)
- (Task)-[:LINKED_TO]->(Settlement)
- (Task)-[:NEEDS_MATERIAL]->(Material)
"""
        return schema


class GraphRAGRetriever:
    """Graph RAG Retriever"""
    
    def __init__(self, neo4j_client: Neo4jGraphClient):
        self.neo4j = neo4j_client
        self.schema = neo4j_client.get_schema()
    
    def retrieve(self, question: str) -> Tuple[str, List[Dict]]:
        """
        根據問題檢索相關圖譜資料
        
        Args:
            question: 使用者問題
            
        Returns:
            Tuple[context, results]
        """
        # 分析問題類型，產生對應的 Cypher
        question_lower = question.lower()
        
        # 問題分類
        if "進度" in question or "progress" in question_lower:
            if "樓層" in question or "floor" in question_lower:
                cypher = self._query_floor_progress(question)
            else:
                cypher = self._query_task_progress(question)
        
        elif "成本" in question or "費用" in question or "price" in question_lower or "cost" in question_lower:
            cypher = self._query_cost(question)
        
        elif "預算" in question or "budget" in question_lower:
            cypher = self._query_budget(question)
        
        elif "結算" in question or "settle" in question_lower:
            cypher = self._query_settlement(question)
        
        else:
            # 預設查詢 - 搜尋相關節點
            cypher = self._query_general(question)
        
        # 執行查詢
        results = self.neo4j.query(cypher)
        
        # 建立 context
        context = self._build_context(results)
        
        return context, results
    
    def _query_floor_progress(self, question: str) -> str:
        """查詢樓層進度"""
        return """
MATCH (p:Project)-[:HAS_FLOOR]->(f:Floor)-[:HAS_TASK]->(t:Task)
RETURN p.name as project, f.floor_name as floor, f.status as floor_status,
       t.name as task, t.progress as progress, t.unit as unit
ORDER BY f.order_num, t.id
"""
    
    def _query_task_progress(self, question: str) -> str:
        """查詢任務進度"""
        return """
MATCH (t:Task)<-[:HAS_TASK]-(f:Floor)
RETURN t.id as task_id, t.name as task, t.progress as progress, 
       t.unit as unit, f.floor_name as floor
"""
    
    def _query_cost(self, question: str) -> str:
        """查詢成本"""
        return """
MATCH (t:Task)<-[:HAS_TASK]-(f:Floor)<-[:HAS_FLOOR]-(p:Project)
OPTIONAL MATCH (t)-[:LINKED_TO]->(s:Settlement)
RETURN p.name as project, f.floor_name as floor, t.name as task,
       t.progress as progress, t.unit_price as unit_price,
       s.amount as settlement_amount, s.status as settlement_status
"""
    
    def _query_budget(self, question: str) -> str:
        """查詢預算"""
        return """
MATCH (p:Project)-[:OWNS]->(b:Budget)
RETURN p.name as project, b.type as budget_type, b.total as total,
       b.reserved as reserved, b.spent as spent,
       toFloat(b.spent) / b.total * 100 as execution_rate
"""
    
    def _query_settlement(self, question: str) -> str:
        """查詢結算單"""
        return """
MATCH (s:Settlement)<-[:LINKED_TO]-(t:Task)<-[:HAS_TASK]-(f:Floor)
RETURN s.id as settlement_id, s.amount as amount, s.date as date,
       s.status as status, s.description as description,
       t.name as task, f.floor_name as floor
"""
    
    def _query_general(self, question: str) -> str:
        """一般搜尋"""
        keywords = question.split()
        search_pattern = " OR ".join([f"toLower(t.name) CONTAINS toLower('{w}')" for w in keywords[:3]])
        
        return f"""
MATCH (t:Task)<-[:HAS_TASK]-(f:Floor)<-[:HAS_FLOOR]-(p:Project)
WHERE {search_pattern}
RETURN p.name as project, f.floor_name as floor, t.name as task, t.progress as progress
LIMIT 5
"""
    
    def _build_context(self, results: List[Dict]) -> str:
        """建立 context 字串"""
        if not results:
            return "No relevant data found in the knowledge graph."
        
        lines = []
        for r in results[:10]:  # 最多 10 筆
            line_parts = []
            for key, value in r.items():
                if value is not None:
                    line_parts.append(f"{key}: {value}")
            lines.append(", ".join(line_parts))
        
        return "\n".join(lines)
    
    def extract_sources(self, results: List[Dict]) -> List[Source]:
        """從查詢結果提取來源"""
        sources = []
        
        for r in results:
            # 從結果中識別來源
            if "task" in r and r["task"]:
                sources.append(Source(
                    node_type="Task",
                    node_id=r.get("task_id", "unknown"),
                    property_name="name",
                    property_value=r["task"],
                    confidence=1.0
                ))
            
            if "floor" in r and r["floor"]:
                sources.append(Source(
                    node_type="Floor",
                    node_id=r.get("floor_id", "unknown"),
                    property_name="floor_name",
                    property_value=r["floor"],
                    confidence=1.0
                ))
            
            if "settlement_id" in r and r["settlement_id"]:
                sources.append(Source(
                    node_type="Settlement",
                    node_id=r["settlement_id"],
                    property_name="amount",
                    property_value=str(r.get("amount", "")),
                    confidence=1.0
                ))
        
        return sources


# Mock 模式的 RAG（無 Neo4j 時使用）
class MockGraphRAGRetriever:
    """Mock Graph RAG Retriever - 用於測試"""
    
    def retrieve(self, question: str) -> Tuple[str, List[Dict]]:
        """回傳 Mock 資料"""
        question_lower = question.lower()
        
        if "進度" in question or "progress" in question_lower:
            results = [
                {"floor": "B1", "task": "鋼筋綁紮", "progress": 100, "unit": "噸"},
                {"floor": "1F", "task": "混凝土澆置", "progress": 80, "unit": "立方公尺"},
                {"floor": "1F", "task": "板模作業", "progress": 60, "unit": "平方公尺"},
            ]
            context = "B1 鋼筋綁紮: 100%\n1F 混凝土澆置: 80%\n1F 板模作業: 60%"
        
        elif "成本" in question or "費用" in question:
            results = [
                {"task": "鋼筋綁紮", "unit_price": 25000, "quantity": 100, "total": 2500000},
                {"task": "混凝土澆置", "unit_price": 3000, "quantity": 200, "total": 600000},
            ]
            context = "鋼筋綁紮: 100噸 x 25,000 = 2,500,000元\n混凝土澆置: 200立方公尺 x 3,000 = 600,000元"
        
        elif "預算" in question:
            results = [
                {"project": "台北信義區豪宅", "total": 500000000, "spent": 120000000, "execution_rate": 24.0},
            ]
            context = "台北信義區豪宅: 總預算 5億，已執行 1.2億 (24%)"
        
        else:
            results = [{"message": "No specific data found for this query"}]
            context = "No relevant data found."
        
        return context, results
    
    def extract_sources(self, results: List[Dict]) -> List[Source]:
        """Mock sources"""
        return [
            Source(node_type="Mock", node_id="mock-001", property_name="data", property_value="mock", confidence=0.9)
        ]


# Factory function
def create_graph_rag_retriever(uri: str = None, user: str = None, password: str = None) -> GraphRAGRetriever:
    """建立 Graph RAG Retriever"""
    uri = uri or os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = user or os.environ.get("NEO4J_USER", "neo4j")
    password = password or os.environ.get("NEO4J_PASSWORD", "")
    
    try:
        neo4j = Neo4jGraphClient(uri, user, password)
        neo4j.connect()
        return GraphRAGRetriever(neo4j)
    except Exception as e:
        print(f"⚠️ 無法連接 Neo4j，使用 Mock 模式: {e}")
        return MockGraphRAGRetriever()


if __name__ == "__main__":
    # 測試
    retriever = create_graph_rag_retriever()
    
    questions = [
        "B1樓層的進度如何？",
        "鋼筋作業的成本多少？",
        "建案預算執行狀況？"
    ]
    
    for q in questions:
        print(f"\n❓ Question: {q}")
        context, results = retriever.retrieve(q)
        print(f"📊 Context: {context}")
        print(f"📋 Results: {results}")
